from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg lavanimi?',
                name='query_test',
                column_name='lavanimi',
                points=5,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg sugu?',
                name='query_test',
                column_name='sugu',
                points=5,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=5,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg punktid_finaalis?',
                name='query_test',
                column_name='punktid_finaalis',
                points=5,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg koht_finaalis?',
                name='query_test',
                column_name='koht_finaalis',
                points=5,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=15,
            ),
            QueryDataTest(
                title='Kas nimekirjas on ainult finalistid?',
                name='query_test',
                column_name='koht_finaalis',
                expected_value="None",
                should_exist=False,
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige järjekord?',
                name='query_test',
                column_name='lavanimi',
                where="test_id=2",
                expected_value="Wrs",
                points=30,
            ),
        ]
    ),
]