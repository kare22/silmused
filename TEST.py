import psycopg2 as psycopg2

from tests.ColumnDataTest import ColumnDataTest
from tests.ColumnExistsTest import ColumnExistsTest
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


connection = connect(db_name='auto_test_kodu6', auto_commit=True)
cursor = connection.cursor()

tests = [
    ColumnDataTest(
        name='mv_partiide_arv_valgetega',
        column_name='*',
        where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'",
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 270',
        expected_value='valge',
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 241',
        expected_value='must',
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 193',
        expected_value='viik',
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='COUNT(*)',
        expected_value=293,
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='COUNT(*)',
        expected_value=299,
        should_exist=False,
        points=1,
    ),
    ColumnDataTest(
        name='v_turniiripartiid',
        column_name='COUNT(*)',
        expected_value=299,
        points=1,
    ),
    ColumnExistsTest(
        name='v_turniiripartiid',
        column_name='partii_id',
        should_exist=False,
        points=1,
    ),
    ColumnExistsTest(
        name='v_turniiripartiid',
        column_name='asdfdsa',
        should_exist=False,
        points=1,
    ),
    ColumnExistsTest(
        name='v_turniiripartiid',
        column_name='partii_id',
        points=1,
    ),
    ColumnExistsTest(
        name='v_turniiripartiid',
        column_name='asdfdsa',
        points=1,
    ),
    ColumnExistsTest(
        name='v_turniiripartiid',
        column_name='kes_voitis',
        points=1,
    ),
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
    FunctionTest(
        name='f_top10',
        arguments=[44],
        where="mangija LIKE 'Murakas%'",
        points=0.25,
    ),
    FunctionTest(
        name='f_top10',
        arguments=[44],
        expected_count=11,
        points=0.25,
    ),
    FunctionTest(
        name='f_top10',
        arguments=[44],
        expected_count=10,
        points=0.25,
    ),
    FunctionTest(
        name='f_top10',
        arguments=[44],
        points=0.25,
    ),
    FunctionTest(
        name='f_top10',
        arguments=[4390],
        points=0.25,
    ),
]

results = []

for test in tests:
    results.append(test.run(cursor))

cursor.close()
connection.close()


for result in results:
    print(f"{result}")