from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='query_test',
                column_name='eesnimi',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='query_test',
                column_name='perenimi',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg sugu?',
                name='query_test',
                column_name='sugu',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg vanus?',
                name='query_test',
                column_name='vanus',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=4,
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige vanus Arvo Metsal?',
                name='query_test',
                column_name='vanus',
                where="eesnimi = 'Arvo' and perenimi = 'Mets'",
                expected_value=85,
                points=30,
            ),
        ]
    ),
]