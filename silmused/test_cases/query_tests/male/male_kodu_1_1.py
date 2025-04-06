from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='query_test',
                column_name='eesnimi',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='query_test',
                column_name='perenimi',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige isik kõige noorem?',
                name='query_test',
                column_name='eesnimi',
                where="test_id=1",
                expected_value="Sander",
                points=30,
            ),
            QueryDataTest(
                title='Kas viies noorim on´õige isik?',
                name='query_test',
                column_name='eesnimi',
                where="test_id=5",
                expected_value="Keiu",
                points=30,
            ),
        ]
    ),
]