from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 4 ülesande 5 päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg linn?',
                name='query_test',
                column_name='linn',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg kokku?',
                name='query_test',
                column_name='kokku',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg maksimaalne?',
                name='query_test',
                column_name='maksimaalne',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=14,
                points=20,
            ),
            QueryDataTest(
                title='Kas järjestus on õige?',
                name='query_test',
                column_name='linn',
                where='test_id=2',
                expected_value="Lisbon",
                points=10,
            ),
            QueryDataTest(
                title='Kas Turinis on õige maksimaalne?',
                name='query_test',
                column_name='kokku',
                where="linn='Turin'",
                expected_value="4640",
                points=10,
            ),
        ]
    ),
]