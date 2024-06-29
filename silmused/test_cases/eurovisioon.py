from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2_1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='test_table',
                column_name='pealkiri',
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='test_table',
                column_name='COUNT(*)',
                expected_value=17,
            ),
            QueryDataTest(
                title='Kas esimesel kohal on õige laul?',
                name='test_table',
                column_name='pealkiri',
                where="id=1",
                expected_value="Love Kills",
            ),
        ]
    ),
]