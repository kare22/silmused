from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 8 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg nimi?',
                name='query_test',
                column_name="nimi",
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=2,
                points=40,
            ),
            QueryDataTest(
                title='Kas on õige linn esimesel kohal?',
                name='query_test',
                column_name='"nimi"',
                where="test_id=1",
                expected_value='Tallinn',
                points=30,
            ),
        ]
    ),
]