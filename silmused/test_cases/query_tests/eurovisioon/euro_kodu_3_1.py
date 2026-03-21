from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg lavanimi?',
                name='query_test',
                column_name='lavanimi',
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=1,
                points=30,
            ),
            QueryDataTest(
                title='Kas puuduva synniajga on Mariko?',
                name='query_test',
                column_name='lavanimi',
                where="test_id=1",
                expected_value="Mariko",
                points=40,
            ),
        ]
    ),
]