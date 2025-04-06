from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 4 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg synniriik_id?',
                name='query_test',
                column_name='synniriik_id',
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
                expected_value=9,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige riigi id esimesel kohal?',
                name='query_test',
                column_name='synniriik_id',
                where="test_id=1",
                expected_value="41",
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige arv riigil id-ga 40?',
                name='query_test',
                column_name='arv',
                where="synniriik_id=40",
                expected_value="13",
                points=30,
            ),
        ]
    ),
]