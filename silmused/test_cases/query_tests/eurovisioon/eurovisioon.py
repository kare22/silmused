from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2_1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=25,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=17,
                points=25,
            ),
            QueryDataTest(
                title='Kas 1. kohal on õige laul?',
                name='query_test',
                column_name='pealkiri',
                where="id=1",
                expected_value="Love Kills",
                points=25,
            ),
            QueryDataTest(
                title='Kas 11. kohal on õige laul?',
                name='query_test',
                column_name='pealkiri',
                where="id=11",
                expected_value="Love",
                points=25,
            ),
        ]
    ),
]