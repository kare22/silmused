from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg lavanimi?',
                name='query_test',
                column_name='lavanimi',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg hetkevanus?',
                name='query_test',
                column_name='hetkevanus',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=12,
                points=30,
            ),
            QueryDataTest(
                title='Kas kõige noorem laulja on Iru?',
                name='query_test',
                column_name='lavanimi',
                where="test_id=1",
                expected_value="Iru",
                points=25,
            ),
            QueryDataTest(
                title='Kas Aiko vanus on õige?',
                name='query_test',
                column_name='hetkevanus',
                where="lavanimi='Aiko'",
                expected_value=[24,25],
                points=25,
            ),
        ]
    ),
]