from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 3 Päringu 2 kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg pealkirja_algus?',
                name='query_test',
                column_name='pealkirja_algus',
                points=20,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg arv?',
                name='query_test',
                column_name='arv',
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=6,
                points=20,
            ),
            QueryDataTest(
                title='Kas leidub pealkirja algus Danc?',
                name='query_test',
                where='"Pealkirja algus"' + "='Danc'",
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige arv "The " algusega pealkirju?',
                name='query_test',
                column_name='"pealkirja_algus"',
                where='arv=15',
                expected_value='The ',
                points=20,
            ),
        ]
    ),
]