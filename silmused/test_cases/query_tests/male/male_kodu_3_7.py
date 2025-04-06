from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 7 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg nimi?',
                name='query_test',
                column_name="nimi",
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg klubide arv?',
                name='query_test',
                column_name="klubide arv",
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
                title='Kas on õige linn kõige suurema klubide arvuga?',
                name='query_test',
                column_name='"klubide arv"',
                where="nimi = 'Tartu'",
                expected_value=6,
                points=30,
            ),
            QueryDataTest(
                title='Kas Elvas on 0 klubi?',
                name='query_test',
                column_name='"klubide arv"',
                where="nimi = 'Elva'",
                expected_value=0,
                points=30,
            ),
        ]
    ),
]