import json
import os
import subprocess
import sys

import psycopg2
from uuid import uuid4
from datetime import datetime
from silmused.version import __version__
from silmused.Translator import Translator
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def _results_to_string(results):
    string = ''
    for result in results:
        if result.get('type') != 'execution' and result.get('message') is not None:
            string += str(result.get('message')) + '\n'

    print(string)


class Runner:
    def __init__(self, backup_file_path, tests, lang='en', test_name='', db_user='postgres', db_host='localhost', db_password='postgresql', db_port='5432', test_query='test', query_sql=None):
        self.file_path = backup_file_path
        self.tests = tests
        self.test_name = test_name
        self.db_user = db_user
        self.db_name = ''
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.test_query = test_query
        self.query_sql = query_sql

        self.db_name = f"db{'_' + self.test_name if self.test_name != '' else ''}_{self.file_path.split('/')[-1].split('.')[0]}_{str(uuid4()).replace('-', '_')}"

        self.results = []
        self.translator = Translator(locale=lang)
        if self.test_query == 'test':
            if self._file_is_valid_pg_dump():
                self._create_db_from_psql_dump()
                self.results = self._run_tests()
                # _results_to_string(self.results)
            elif self._file_is_valid_pg_insert():
                self._create_db_from_psql_insert()
                self.results = self._run_tests()
                # _results_to_string(self.results)
            else:
                print('Error: File is not a valid PostgresSql dump or insert file!')
        elif self.test_query == 'query':
            # print('Query Test is selected!')
            if self._file_is_valid_pg_dump():
                self._create_db_from_psql_dump()
                self._create_query_view()
                self.results = self._run_tests()
            elif self._file_is_valid_pg_insert():
                self._create_db_from_psql_insert()
                self._create_query_view()
                self.results = self._run_tests()
            else:
                print('Error: File is not a valid PostgresSql dump or insert file!')
        else:
            print('Error: Choose Test or Query format!')

    def _file_is_valid_pg_dump(self):
        if not os.path.isfile(self.file_path):
            return False

        try:
            with open(self.file_path, 'rb') as file:
                magic_number = file.read(5)
                return magic_number == b'PGDMP'
        except IOError:
            return False

    def _create_db_from_psql_dump(self):
        subprocess.run(["createdb", "-U", self.db_user, self.db_name])

        subprocess.run(
            ["psql", "-U", self.db_user, "-d", self.db_name, "-c", "DROP SCHEMA public CASCADE;"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        subprocess.run(
            ["pg_restore", "-U", self.db_user, "-d", self.db_name, "--no-owner", "--no-acl", "-1", self.file_path]
        )

    def _file_is_valid_pg_insert(self):
        if not os.path.isfile(self.file_path):
            return False

        if not self.file_path.lower().endswith('.sql'):
            return False

        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                return any(line.strip().startswith("INSERT") for line in lines)
        except IOError:
            return False

    def _create_db_from_psql_insert(self):
        connection = self._connect(db_name='postgres')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        try:
            cursor.execute(f"CREATE DATABASE {self.db_name};")
        except Exception as exception:
            print(f"CREATE DATABASE failed: {exception}")
        finally:
            cursor.close()
            connection.close()

        connection = self._connect()
        cursor = connection.cursor()

        try:
            with open(self.file_path, 'r') as file:
                sql_script = file.read()
            cursor.execute('DROP SCHEMA IF EXISTS public')
            cursor.execute(sql_script)
            connection.commit()
        except Exception as exception:
            print(f"Sql INSERT import failed: {exception}")
        finally:
            cursor.close()
            connection.close()

    def _run_tests(self):
        connection = self._connect()
        cursor = connection.cursor()

        try:
            results = []

            for test in self.tests:
                results.append(test.run(cursor))

            return results
        except Exception as exception:
            print(f"Sql TEST RUN failed: {exception}")
        finally:
            cursor.close()
            connection.close()

    def _create_query_view(self):
        connection = self._connect()
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE VIEW test AS " + self.query_sql)
            connection.commit()
        except Exception as exception:
            print(f"Running SQL failed: {exception}")
        finally:
            cursor.close()
            connection.close()

    def _connect(self, db_name=None):
        connection_layer = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name if db_name is None else db_name,
            user=self.db_user,
            password=self.db_password
        )

        return connection_layer

    def _message_to_feedback(self, message):
        feedback = ''
        feedback_params = [key for key, value in message.items() if key not in ['test_type', 'test_key']]
        if len(feedback_params) > 0:
            params = message['params']
            if len(params) == 0:
                feedback = self.translator.translate(message['test_type'], message['test_key'])

            elif len(params) == 1:
                feedback = self.translator.translate(message['test_type'], message['test_key'],
                                                     param1=params[0])
            elif len(params) == 2:
                feedback = self.translator.translate(message['test_type'], message['test_key'],
                                                     param1=params[0], param2=params[1])
            elif len(params) == 3:
                feedback = self.translator.translate(message['test_type'], message['test_key'],
                                                     param1=params[0], param2=params[1], param3=params[2])
            elif len(params) == 4:
                feedback = self.translator.translate(message['test_type'], message['test_key'],
                                                     param1=params[0], param2=params[1], param3=params[2], param4=params[3])
            else:
                feedback = "Params were given, but there is more than 4"

        return feedback

    def _checks_to_object(self, checks):
        outputs = []
        output_pass = True


        # TODO should be recursive
        points_max = 0
        points_actual = 0

        for check in checks:
            if check.get('type') == 'execution':
                continue
            elif check.get('type') == 'message':
                outputs.append({
                    "title": str(check.get('message')),
                    "status": 'PASS'
                })
                continue

            points = check.get('points') if check.get('points') is not None else 0
            points_max += points
            points_actual += points if check.get('is_success') else 0

            output = {}
            output["title"] = check.get('title')
            output["status"] = 'PASS' if check.get('is_success') else 'FAIL'
            output_pass = True if check.get('is_success') and output_pass else False
            if not check.get('is_success') and not check.get('is_sys_fail'):
                output["feedback"] = self._message_to_feedback(check.get('message'))
            elif check.get('is_sys_fail'):
                output["feedback"] = str(check.get('message'))
            else:
                output["feedback"] = ''
            outputs.append(output)

        return points_max, points_actual, outputs, output_pass

    def _results_to_object(self):
        tests = []

        points_max = 0
        points_actual = 0

        for result in self.results:
            if result.get('type') == 'execution':
                continue
            elif result.get('type') == 'message':
                tests.append({
                    "title": str(result.get('message')),
                    "status": 'PASS'
                })
                continue

            output = {}

            if result.get('type') == 'checks_layer':
                checks_points_max, checks_points_actual, checks_outputs, output_pass = self._checks_to_object(result.get('checks'))
                points_max += checks_points_max
                points_actual += checks_points_actual
                output["checks"] = checks_outputs
                output["status"] = 'PASS' if output_pass else 'FAIL'
            else:
                points = result.get('points') if result.get('points') is not None else 0
                points_max += points
                points_actual += points if result.get('is_success') else 0
                output["status"] = 'PASS' if result.get('is_success') else 'FAIL'

            output["title"] = result.get('title')
            if result.get('message') is not None:
                output["exception_message"] = str(result.get('message'))

            tests.append(output)
        return tests, points_max, points_actual

    def get_results(self):
        try:
            tests, points_max, points_actual = self._results_to_object()
            # TODO Put all logic in points variable
            praks = True if len(tests) > 0 and points_max == 0 and points_actual == 0 else False
            if praks:
                points_max = 1
                points_actual = 1

            output = {
                "result_type": "OK_V3",
                "points": round(100 * points_actual / points_max),
                "producer": f"silmused {__version__}",
                "finished_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tests": tests
            }
            return json.dumps(output, ensure_ascii=False)
        except:
            print(sys.exc_info())
            return json.dumps({
              "result_type": "OK_V3",
              "producer": f"silmused {__version__}",
              "finished_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
              "points": 0,
            }, ensure_ascii=False)