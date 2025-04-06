from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg riik?',
                name='query_test',
                column_name='riik',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg lauljate arv?',
                name='query_test',
                column_name='lauljate arv',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=3,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige järjekord?',
                name='query_test',
                column_name='"riik"',
                where="test_id=2",
                expected_value="Portugal",
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige lauljate arv United Kingdom-is?',
                name='query_test',
                column_name='"lauljate arv"',
                where="test_id=1",
                expected_value="17",
                points=30,
            ),
        ]
    ),
]