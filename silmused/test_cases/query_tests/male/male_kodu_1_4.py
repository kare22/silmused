from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 4 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg ränkingu klass?',
                name='query_test',
                column_name="sünnikuu number",
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg arv?',
                name='query_test',
                column_name='arv',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=3,
                points=30,
            ),
            QueryDataTest(
                title='Kas on mais kõige vähem mängijaid?',
                name='query_test',
                column_name='arv',
                where='"sünnikuu number" = 5',
                expected_value=2,
                points=30,
            ),
        ]
    ),
]