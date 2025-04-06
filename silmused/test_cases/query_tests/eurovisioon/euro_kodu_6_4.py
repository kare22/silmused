from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 4 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkirja_algus?',
                name='query_test',
                column_name='pealkirja_algus',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg laulude_arv?',
                name='query_test',
                column_name='laulude_arv',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=1,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige laulu pealkirja algus?',
                name='query_test',
                column_name='pealkirja_algus',
                where="test_id=1",
                expected_value='Love ',
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige laulude arv?',
                name='query_test',
                column_name='"laulude_arv"',
                where="test_id=1",
                expected_value=9,
                points=30,
            ),
        ]
    ),
]