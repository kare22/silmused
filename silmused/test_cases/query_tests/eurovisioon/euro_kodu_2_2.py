from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg id?',
                name='query_test',
                column_name='id',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg linn?',
                name='query_test',
                column_name='linn',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg finaali_kuupaev?',
                name='query_test',
                column_name='finaali_kuupaev',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg riik_id?',
                name='query_test',
                column_name='riik_id',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=30,
            ),
            QueryDataTest(
                title='Kas kontroll linn on olemas?',
                name='query_test',
                column_name='linn',
                where="id=3",
                expected_value="Stockholm",
                points=30,
            ),
        ]
    ),
]