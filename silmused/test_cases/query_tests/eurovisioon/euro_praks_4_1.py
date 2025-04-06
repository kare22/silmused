from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 4 ülesande 1 päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg lavanimi?',
                name='query_test',
                column_name='lavanimi',
                points=30,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg nimi?',
                name='query_test',
                column_name='nimi',
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=631,
                points=30,
            ),
            QueryDataTest(
                title='Kas on lauljal Kaleen õige sünniriik?',
                name='query_test',
                column_name='nimi',
                where="lavanimi='Kaleen'",
                expected_value="Austria",
                points=10,
            ),
        ]
    ),
]