from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 4 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg riikide arv?',
                name='query_test',
                column_name='riikide arv',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg keskmine rahvaarv?',
                name='query_test',
                column_name='keskmine rahvaarv',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=1,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige riikide arv?',
                name='query_test',
                column_name='"riikide arv"',
                expected_value="3",
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige keskmine?',
                name='query_test',
                column_name='"keskmine rahvaarv"',
                expected_value="1799472.333333333333",
                points=20,
            ),
        ]
    ),
]