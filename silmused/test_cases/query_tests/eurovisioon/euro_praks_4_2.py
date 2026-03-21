from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 4 ülesande 2 päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg punktid_finaalis?',
                name='query_test',
                column_name='punktid_finaalis',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg koht_finaalis?',
                name='query_test',
                column_name='koht_finaalis',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=15,
                points=20,
            ),
            QueryDataTest(
                title='Kas leidub laul Kuula?',
                name='query_test',
                where="pealkiri='Kuula'",
                points=10,
            ),
            QueryDataTest(
                title='Kas puudub laulu Verona finaali koht?',
                name='query_test',
                column_name='koht_finaalis',
                where="pealkiri='Verona'",
                expected_value='None',
                points=10,
            ),
        ]
    ),
]