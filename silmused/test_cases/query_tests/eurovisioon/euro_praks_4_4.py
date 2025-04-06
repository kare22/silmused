from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 4 ülesande 4 päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg nimi?',
                name='query_test',
                column_name='nimi',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg pealkiri?',
                name='query_test',
                column_name='pealkiri',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=41,
                points=20,
            ),
            QueryDataTest(
                title='Kas laul "Roi" on õigest riigist?',
                name='query_test',
                column_name='nimi',
                where="pealkiri='Roi'",
                expected_value='France',
                points=20,
            ),
        ]
    ),
]