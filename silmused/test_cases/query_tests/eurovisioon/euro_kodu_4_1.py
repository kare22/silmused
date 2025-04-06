from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg linn?',
                name='query_test',
                column_name='linn',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg aasta?',
                name='query_test',
                column_name='aasta',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='võidulaul',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=15,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige laul viimasel kohal?',
                name='query_test',
                column_name='võidulaul',
                where="test_id=15",
                expected_value="The Code",
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige võiduaasta Heroes laulul?',
                name='query_test',
                column_name='aasta',
                where="võidulaul='Heroes'",
                expected_value="2015",
                points=30,
            ),
        ]
    ),
]