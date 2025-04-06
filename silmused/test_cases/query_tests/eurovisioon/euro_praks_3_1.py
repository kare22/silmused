from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest

tests = [
    ChecksLayer(
        title='Praktikum 3 Päringu 1 kontrollid',
        tests=[
            QueryDataTest(
                title='Kas on õige tulemuste järjekord?',
                name='query_test',
                column_name='keel',
                where="test_id=1",
                expected_value="French",
                points=20,
            ),
            QueryDataTest(
                title='Kas on õige arv French keelelisi laule?',
                name='query_test',
                column_name='arv',
                where="keel='French'",
                expected_value="11",
                points=20,
            ),
        ]
    ),
]