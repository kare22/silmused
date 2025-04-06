from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg ränkingu klass?',
                name='query_test',
                column_name="ränkingu klass",
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
                expected_value=4,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige arv mängijaid ränkinguga 1000?',
                name='query_test',
                column_name='arv',
                where='"ränkingu klass" = 1000',
                expected_value=25,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ränking viimasel kohal?',
                name='query_test',
                column_name='"ränkingu klass"',
                where='test_id=4',
                expected_value=1300,
                points=20,
            ),
        ]
    ),
]