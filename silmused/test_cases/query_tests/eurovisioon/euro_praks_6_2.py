from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 6 ülesande 2 päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg aasta?',
                name='query_test',
                column_name='aasta',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg esineja?',
                name='query_test',
                column_name='esineja',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg laul?',
                name='query_test',
                column_name='laul',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg keel?',
                name='query_test',
                column_name='keel',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg punktid?',
                name='query_test',
                column_name='punktid',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg koht?',
                name='query_test',
                column_name='koht',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=19,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige järjekord?',
                name='query_test',
                column_name='aasta',
                where="test_id=4",
                expected_value='2011',
                points=10,
            ),
            QueryDataTest(
                title='Kas on punktid puudu esinejal Manpower?',
                name='query_test',
                column_name='punktid',
                where="esineja='Manpower 4'",
                expected_value='None',
                points=10,
            ),
        ]
    ),
]