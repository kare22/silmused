from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg riik_id?',
                name='query_test',
                column_name='riik_id',
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
                expected_value=4,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige riigi id esimesel kohal?',
                name='query_test',
                column_name='riik_id',
                where="test_id=1",
                expected_value="3",
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige arv riigil id-ga 2?',
                name='query_test',
                column_name='arv',
                where="riik_id=2",
                expected_value="6",
                points=30,
            ),
        ]
    ),
]