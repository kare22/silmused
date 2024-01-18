import json
import os
import subprocess
import sys

import psycopg2
from uuid import uuid4
from datetime import datetime
from silmused.version import __version__

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def _results_to_string(results):
    string = ''
    for result in results:
        if result.get('type') is not 'execution' and result.get('message') is not None:
            string += str(result.get('message')) + '\n'

    print(string)


class Runner:
    def __init__(self, backup_file_path, tests, lang='en', test_name='', db_user='postgres', db_host='localhost', db_password='postgresql', db_port='5432'):
        self.file_path = backup_file_path
        self.tests = tests
        self.test_name = test_name
        self.db_user = db_user
        self.db_name = ''
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.lang = lang

        self.db_name = f"db{'_' + self.test_name if self.test_name != '' else ''}_{self.file_path.split('/')[-1].split('.')[0]}_{str(uuid4()).replace('-', '_')}"

        self.results = []

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

    def _connect(self, db_name=None):
        connection_layer = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name if db_name is None else db_name,
            user=self.db_user,
            password=self.db_password
        )

        return connection_layer

    def _results_to_object(self):
        tests = []

        points_max = 0
        points_actual = 0

        for result in self.results:
            if result.get('type') is 'execution':
                continue
            elif result.get('type') is 'message':
                tests.append({
                    "title": str(result.get('message')),
                    "status": 'PASS'
                })
                continue

            points = result.get('points') if result.get('points') is not None else 0
            points_max += points
            points_actual += points if result.get('is_success') else 0

            tests.append({
                "title": result.get('title'), #TODO result needs a title
                "status": 'PASS' if result.get('is_success') else 'FAIL',
                "exception_message": 'Error msg' if not result.get('is_success') else None,
            })

        return tests, points_max, points_actual

    def get_results(self):
        # TODO add json to dependencies
        try:
            tests, points_max, points_actual = self._results_to_object()

            message = {
                "result_type": "OK_V3",
                "points": (points_actual / points_max) * 100,
                "producer": f"silmused {__version__}", #TODO add version
                "finished_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), #TODO
                "tests": tests
            }

            output = {
                "message_type": "OK_V3",
                "message": message,
            }
            return json.dumps(output)
        except:
            print(sys.exc_info())
            return json.dumps({
              "message_type": "ERROR_V3",
              "message":
              {
                "error": "Failed to get results"
              }
            })