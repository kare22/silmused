import os
import subprocess
import psycopg2
from uuid import uuid4


def _results_to_string(results):
    string = ''
    for result in results:
        if result.get('type') is not 'execution' and result.get('message') is not None:
            string += str(result.get('message')) + '\n'

    print(string)


class Runner:
    def __init__(self, file_path, tests, lang='en', test_name='', db_user='postgres', db_host='localhost', db_password='postgresql', db_port='5432'):
        self.file_path = file_path
        self.tests = tests
        self.test_name = test_name
        self.db_user = db_user
        self.db_name = ''
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.lang = lang

        self.db_name = f"db{'_' + self.test_name if self.test_name != '' else ''}_{self.file_path.split('/')[-1].split('.')[0]}_{str(uuid4()).replace('-', '_')}"

        if self._file_is_valid_pg_dump():
            self._create_db_from_backup()
            _results_to_string(self._run_tests())
        else:
            print('Error: File is not a valid PostgreSql dump file!')

    def _file_is_valid_pg_dump(self):
        if not os.path.isfile(self.file_path):
            return False

        try:
            with open(self.file_path, 'rb') as file:
                magic_number = file.read(5)
                return magic_number == b'PGDMP'
        except IOError:
            return False

    def _create_db_from_backup(self):
        subprocess.run(["createdb", "-U", self.db_user, self.db_name])

        subprocess.run(
            ["psql", "-U", self.db_user, "-d", self.db_name, "-c", "DROP SCHEMA public CASCADE;"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        subprocess.run(
            ["pg_restore", "-U", self.db_user, "-d", self.db_name, "--no-owner", "--no-acl", "-1", self.file_path]
        )

    def _run_tests(self):
        connection = self._connect()
        cursor = connection.cursor()

        results = []

        for test in self.tests:
            results.append(test.run(cursor))

        cursor.close()
        connection.close()

        return results

    def _connect(self):
        connection_layer = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

        return connection_layer

