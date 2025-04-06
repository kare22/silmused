from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg nimi?',
                name='query_test',
                column_name="nimi",
                points=15,
            ),
            QueryStructureTest(
                title='Kas on olemas ainult veerg nimi?',
                name='query_test',
                column_name=["asukoht", "id"],
                should_exist=False,
                points=15,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=4,
                points=40,
            ),
            QueryDataTest(
                title='Kas on olemas klubi Ajurebend?',
                name='query_test',
                column_name='COUNT(*)',
                where="nimi = 'Ajurebend'",
                expected_value=1,
                points=15,
            ),
            QueryDataTest(
                title='Kas ei ole olemas klubi Laudnikud?',
                name='query_test',
                column_name='COUNT(*)',
                where="nimi = 'Laudnikud'",
                expected_value=0,
                points=15,
            ),
        ]
    ),
]