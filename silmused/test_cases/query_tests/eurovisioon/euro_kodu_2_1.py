from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=10,
                points=20,
            ),
            QueryDataTest(
                title='Kas 1. kohal on õige laul?',
                name='query_test',
                column_name='pealkiri',
                where="test_id=1",
                expected_value="Madness of Love",
                points=30,
            ),
            QueryDataTest(
                title='Kas 8. kohal on õige laul?',
                name='query_test',
                column_name='pealkiri',
                where="test_id=8",
                expected_value="LoveWave",
                points=30,
            ),
        ]
    ),
]