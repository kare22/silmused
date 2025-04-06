from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg lavanimi?',
                name='query_test',
                column_name='lavanimi',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg sünniriik?',
                name='query_test',
                column_name='sünniriik',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg arv?',
                name='query_test',
                column_name='arv',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=17,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige laulja 8. kohal?',
                name='query_test',
                column_name='lavanimi',
                where="test_id=8",
                expected_value='Lena',
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige suurim osalemisarv?',
                name='query_test',
                column_name='arv',
                where="lavanimi='Valentina Monetta'",
                expected_value='4',
                points=20,
            ),
        ]
    ),
]