from silmused.ChecksLayer import ChecksLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest


tests = [
    ChecksLayer(
        title='Ülesanne 1 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='test',
                column_name='eesnimi',
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='test',
                column_name='perenimi',
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='test',
                column_name='COUNT(*)',
                expected_value=5,
            ),
            QueryDataTest(
                title='Kas on olemas Sander Saabas?',
                name='test',
                column_name='eesnimi',
                where="perenimi='Saabas'",
            ),
        ]
    ),
    ChecksLayer(
        title='Ülesanne 2 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg eesnimi?',
                name='test',
                column_name='eesnimi',
            ),
            QueryStructureTest(
                title='Kas on olemas veerg perenimi?',
                name='test',
                column_name='perenimi',
            ),
            QueryStructureTest(
                title='Kas on olemas veerg sugu?',
                name='test',
                column_name='sugu',
            ),
            QueryStructureTest(
                title='Kas on olemas veerg vanus?',
                name='test',
                column_name='vanus',
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='test',
                column_name='COUNT(*)',
                expected_value=4,
            ),
            QueryDataTest(
                title='Kas on olemas Arvo Mets õige vanusega?',
                name='test',
                where="eesnimi = 'Arvo' and perenimi = 'Mets' and vanus = (select extract( year from age(current_date,synniaeg)) from isikud where eesnimi = 'Arvo' and perenimi = 'Mets')",
            ),
        ]
    ),
]