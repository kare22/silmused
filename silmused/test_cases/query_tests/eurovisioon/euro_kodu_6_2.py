from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg riik?',
                name='query_test',
                column_name='riik',
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=6,
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige riik kõige väiksema osalusega?',
                name='query_test',
                column_name='"riik"',
                where="test_id=1",
                expected_value='Andorra',
                points=30,
            ),
            QueryDataTest(
                title='Kas on olemas riik Australia?',
                name='query_test',
                where="riik='Australia'",
                points=30,
            ),
            QueryDataTest(
                title='Kas ei ole olemas riiki Bulgaaria?',
                name='query_test',
                where="riik='Bulgaria'",
                should_exist=False,
                points=30,
            ),
        ]
    ),
]