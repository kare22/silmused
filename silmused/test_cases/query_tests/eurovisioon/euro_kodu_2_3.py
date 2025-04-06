from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg laulude arv?',
                name='query_test',
                column_name='laulude arv',
                points=40,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=1,
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige laulude arv?',
                name='query_test',
                column_name='"laulude arv"',
                expected_value="124",
                points=30,
            ),
        ]
    ),
]