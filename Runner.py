import subprocess

import psycopg2


class Runner:
    def __init__(self, file_path, tests, test_name='', db_user='postgres', db_host='localhost', db_password='postgresql', db_port='5432'):
        self.file_path = file_path
        self.tests = tests
        self.test_name = test_name
        self.db_user = db_user
        self.db_name = ''
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self._create_db_from_backup()
        self._run_tests()

    def _database_exists(self):
        result = subprocess.run(
            ["psql", "-U", self.db_user, "-tAc", f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'"], capture_output=True, text=True)
        return result.stdout.strip() == '1'

    def _drop_database(self):
        subprocess.run(["dropdb", "-U", self.db_user, self.db_name])

    def _create_db_from_backup(self):
        self.db_name = f"db_{self.file_path.split('/')[-1].split('.')[0]}{'_' + self.test_name if self.test_name != '' else ''}"

        if self._database_exists():
            self._drop_database()

        subprocess.run(["createdb", "-U", self.db_user, self.db_name])

        subprocess.run(["psql", "-U", self.db_user, "-d", self.db_name, "-c", "DROP SCHEMA public CASCADE;"])

        subprocess.run(["pg_restore", "-U", self.db_user, "-d", self.db_name, "--no-owner", "--no-acl", "-1", self.file_path])

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