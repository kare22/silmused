from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='query_test',
                column_name="eesnimi",
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='query_test',
                column_name="perenimi",
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg keskmine tulemus?',
                name='query_test',
                column_name="keskmine tulemus",
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg nupu värv?',
                name='query_test',
                column_name="nupu värv",
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=160,
                points=10,
            ),
            QueryDataTest(
                title='Kas on NULL tulemus mustaga mängijal Heli Jälg?',
                name='query_test',
                column_name='"keskmine tulemus"',
                where="eesnimi = 'Heli' and perenimi = 'Jälg'",
                expected_value='NULL',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige keskmine valgega mängijal Kalev Jõud?',
                name='query_test',
                column_name='round("keskmine tulemus",0)',
                where="eesnimi = 'Kalev' and test_id=54",
                expected_value=1,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige keskmine eespool mängijal Andrei Sosnov?',
                name='query_test',
                column_name='"nupu värv"',
                where="test_id=7",
                expected_value='must',
                points=10,
            ),
        ]
    ),
]