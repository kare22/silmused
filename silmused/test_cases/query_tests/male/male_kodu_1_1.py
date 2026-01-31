from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='query_test',
                column_name='eesnimi',
                points=15,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='query_test',
                column_name='perenimi',
                points=15,
            ),
            QueryStructureTest(
                title='Kas lahenduses on ainult 2 veergu?',
                name='query_test',
                column_name=['id','isikukood','klubi','synniaeg','sugu','ranking'],
                should_exist=False,
                points=10,
            ),
            QueryStructureTest(
                title='Kas lahenduses on kasutatud LIMITit?',
                name='query_test',
                elements='LIMIT',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige isik kõige noorem?',
                name='query_test',
                column_name='eesnimi',
                where="test_id=1",
                expected_value="Sander",
                points=20,
            ),
            QueryDataTest(
                title='Kas viies noorim on´õige isik?',
                name='query_test',
                column_name='eesnimi',
                where="test_id=5",
                expected_value="Keiu",
                points=20,
            ),
        ]
    ),
]