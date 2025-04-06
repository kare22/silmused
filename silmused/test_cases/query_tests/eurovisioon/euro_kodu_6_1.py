from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg riik?',
                name='query_test',
                column_name='riik',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg laulude arv?',
                name='query_test',
                column_name='laulude arv',
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg keskmine punktisumma?',
                name='query_test',
                column_name='keskmine punktisumma',
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
                title='Kas on õige arv laule Eestil jõudnud finaali?',
                name='query_test',
                column_name='"laulude arv"',
                where="riik='Estonia'",
                expected_value=10,
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige keskmine punktisumma Soomel?',
                name='query_test',
                column_name='ROUND("keskmine punktisumma",1)',
                where="riik='Finland'",
                expected_value=123.7,
                points=20,
            ),
        ]
    ),
]