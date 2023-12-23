import psycopg2 as psycopg2

from tests.FunctionTest import FunctionTest
from tests.VIewTest import ViewTest

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "karelpaan"
DB_PASSWORD = "postgresql"
DB_SCHEMA = "public"


def connect(db_name='postgres', auto_commit=False):
    connection_layer = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=db_name,
        user=DB_USER,
        password=DB_PASSWORD
    )

    if auto_commit:
        connection_layer.autocommit = True

    return connection_layer


connection = connect(db_name='auto_test', auto_commit=True)
cursor = connection.cursor()

tests = [
    ViewTest(
        name='v_turniiripartiid',
        points=1,
    ),
    ViewTest(
        name='v_turniiripartiidasdf',
        points=1,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        expected_value=1279.6,
        points=0.25,
        description='tere maailm'
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        points=0.25,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        expected_count=1,
        points=0.25,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[56],
        expected_value=1279.6,
        points=0.25,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        expected_count=3,
        points=0.25,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        expected_value='1279.6',
        points=0.25,
    ),
    FunctionTest(
        name='awewfewe',
        arguments=[54],
        expected_value='1279.6',
        points=0.25,
    ),
]

results = []

for test in tests:
    results.append(test.execute(cursor))

cursor.close()
connection.close()


print(results)