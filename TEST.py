import psycopg2 as psycopg2

from TitleLayer import TitleLayer
from tests.ColumnDataTest import ColumnDataTest
from tests.ColumnStructureTest import ColumnStructureTest
from tests.ConstraintTest import ConstraintTest
from tests.FunctionTest import FunctionTest
from tests.IndexTest import IndexTest
from tests.ProcedureTest import ProcedureTest
from tests.TriggerTest import TriggerTest
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
    TitleLayer('Praktikum 3'),
    ColumnStructureTest(
        name='turniirid',
        column_name='asukoht',
        points=2,
    ),
    ColumnStructureTest(
        name='partiid',
        column_name='vastavus',
        points=1,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='un_isikukood',
        constraint_type='UNIQUE',
        points=0.25,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='nimi_unique',
        constraint_type='UNIQUE',
        should_exist=False,
        points=0.5,
    ),
    ColumnStructureTest(
        name='klubid',
        column_name='asukoht',
        arguments=['character_maximum_length'],
        expected_value=100,
        points=1,
    ),
    ColumnStructureTest(
        name='klubid',
        column_name='asukoht',
        points=1,
    ),
    #
    # IndexTest(
    #     name='ewojifewoifejw',
    # ),
    # IndexTest(
    #     name='ix_riiginimi',
    # ),
    # IndexTest(
    #     name='ix_suurus',
    # ),
    # TriggerTest(
    #     name='tg_klubi_olemasolu',
    #     arguments=['UPDATE', 'INSERT', 'jifweo', 'wewwe'],
    #     action_timing='BEFORE'
    # ),
    # TriggerTest(
    #     name='tg_partiiaeg',
    #     arguments=['UPDATE', 'INSERT'],
    #     action_timing='BEFORE'
    # ),
    # TitleLayer('See on ilus tiitel'),
    # ProcedureTest(
    #     name='sp_uus_turniir',
    #     arguments=['Tartu Meister', '02.02.2022', 1, 'Tartu'],
    #     number_of_columns=4,
    #     pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
    #     after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.03.2022'",
    #     points=1,
    # ),
    # ProcedureTest(
    #     name='sp_uus_turniir',
    #     arguments=['Tartu Meister', '02.02.2022', 2, 'Tartu'],
    #     number_of_columns=4,
    #     pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
    #     after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.04.2022'",
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='mv_partiide_arv_valgetega',
    #     column_name='*',
    #     where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'",
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='LOWER(kes_voitis)',
    #     where='partii_id = 270',
    #     expected_value='valge',
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='LOWER(kes_voitis)',
    #     where='partii_id = 241',
    #     expected_value='must',
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='LOWER(kes_voitis)',
    #     where='partii_id = 193',
    #     expected_value='viik',
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='COUNT(*)',
    #     expected_value=293,
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='COUNT(*)',
    #     expected_value=299,
    #     should_exist=False,
    #     points=1,
    # ),
    # ColumnDataTest(
    #     name='v_turniiripartiid',
    #     column_name='COUNT(*)',
    #     expected_value=299,
    #     points=1,
    # ),
    # ColumnStructureTest(
    #     name='v_turniiripartiid',
    #     column_name='partii_id',
    #     should_exist=False,
    #     points=1,
    # ),
    # ColumnStructureTest(
    #     name='v_turniiripartiid',
    #     column_name='asdfdsa',
    #     should_exist=False,
    #     points=1,
    # ),
    # ColumnStructureTest(
    #     name='v_turniiripartiid',
    #     column_name='partii_id',
    #     points=1,
    # ),
    # ColumnStructureTest(
    #     name='v_turniiripartiid',
    #     column_name='asdfdsa',
    #     points=1,
    # ),
    # ColumnStructureTest(
    #     name='v_turniiripartiid',
    #     column_name='kes_voitis',
    #     points=1,
    # ),
    # ViewTest(
    #     name='v_turniiripartiid',
    #     points=1,
    # ),
    # ViewTest(
    #     name='v_turniiripartiidasdf',
    #     points=1,
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[54],
    #     expected_value=1279.6,
    #     points=0.25,
    #     description='tere maailm'
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[54],
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[54],
    #     expected_count=1,
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[56],
    #     expected_value=1279.6,
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[54],
    #     expected_count=3,
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_klubiranking',
    #     arguments=[54],
    #     expected_value='1279.6',
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='awewfewe',
    #     arguments=[54],
    #     expected_value='1279.6',
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_top10',
    #     arguments=[44],
    #     where="mangija LIKE 'Murakas%'",
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_top10',
    #     arguments=[44],
    #     expected_count=11,
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_top10',
    #     arguments=[44],
    #     expected_count=10,
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_top10',
    #     arguments=[44],
    #     points=0.25,
    # ),
    # FunctionTest(
    #     name='f_top10',
    #     arguments=[4390],
    #     points=0.25,
    # ),
]

results = []

for test in tests:
    results.append(test.run(cursor))

cursor.close()
connection.close()


for result in results:
    print(f"{result}")