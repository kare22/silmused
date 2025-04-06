from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Agregeeriva Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg arv?',
                name='query_test',
                column_name='arv',
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=1,
                points=40,
            ),
            QueryDataTest(
                title='Kas on õige riikide arv?',
                name='query_test',
                column_name='arv',
                expected_value="4",
                points=30,
            ),
        ]
    ),
]