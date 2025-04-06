from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Mitte Agregeeriva Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=25,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=25,
            ),
            QueryDataTest(
                title='Kas leidub laul "Nova Deca"?',
                name='query_test',
                column_name='pealkiri',
                where="pealkiri = 'Nova deca'",
                points=25,
            ),
            QueryDataTest(
                title='Kas leidub laul "Eaea"?',
                name='query_test',
                column_name='pealkiri',
                where="pealkiri = 'Eaea'",
                points=25,
            ),
        ]
    ),
]