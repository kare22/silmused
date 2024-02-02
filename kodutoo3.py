from silmused.TitleLayer import TitleLayer
from silmused.ChecksLayer import ChecksLayer
from silmused.ExecuteLayer import ExecuteLayer
from silmused.tests.DataTest import DataTest
from silmused.tests.StructureTest import StructureTest
from silmused.tests.ConstraintTest import ConstraintTest
from silmused.tests.FunctionTest import FunctionTest
from silmused.tests.IndexTest import IndexTest
from silmused.tests.ProcedureTest import ProcedureTest
from silmused.tests.TriggerTest import TriggerTest
from silmused.tests.ViewTest import ViewTest

tests = [
    # Praktikumis tehtud asjade kontroll
    ChecksLayer(
        title='Tabeli Isikud kontrollid ',
        tests=[
            StructureTest(
                title='Kas tabel Isikud on olemas?',
                name='isikud',
            ),
        ]
    ),
]
"""ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='isikud',
                constraint_type='PRIMARY KEY',
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='isikud',
                constraint_type='UNIQUE',
            ),
            ConstraintTest(
                title='Kas tabelis on check kitsendus?',
                name='isikud',
                constraint_type='CHECK',
            ),"""

"""
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='klubid',
                column_name='asukoht',
                should_exist=False,
            ),
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='klubid',
                column_name='toimumiskoht',
                should_exist=False,
            ),

        ]
    ),
    # Ülesanne 1 ja 2, hetkel see kontroll on katki, pean uurima
    ChecksLayer(
        title='Tabeli Inimesed kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel Inimesed on olemas?',
                name='inimesed',
                points=1,
            ),
            StructureTest(
                title='Kas veerg eesnimi on olemas?',
                name='inimesed',
                column_name='eesnimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg perenimi on olemas?',
                name='inimesed',
                column_name='perenimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg sugu on olemas?',
                name='inimesed',
                column_name='sugu',
                points=1,
            ),
            ConstraintTest(
                title='Kas veerul sugu on check kitsendus?',
                name='inimesed',
                column_name='sugu',
                constraint_type='CHECK',
                points=1,
            ),
            StructureTest(
                title='Kas veerg synnipaev on olemas?',
                name='inimesed',
                column_name='synnipaev',
                points=1,
            ),
            StructureTest(
                title='Kas veerg sisestatud on olemas?',
                name='inimesed',
                column_name='sisestatud',
                points=1,
            ),
            StructureTest(
                title='Kas veerg isikukood on olemas?',
                name='inimesed',
                column_name='isikukood',
                points=1,
            ),
            ConstraintTest(
                title='Kas veerul isikukood on unikaalsuse kitsendus?',
                name='inimesed',
                column_name='isikukood',
                constraint_type='UNIQUE',
                points=1,
            ),
            DataTest(
                title='Kas tabelis inimesed on andmed olemas?',
            name='inimesed',
            points=1,
            ),
        ]
    ),
    # Ülesande 3, 4, 5, 6 kontroll
    ChecksLayer(
        title='Tabeli Turniirid kontrollid',
        tests=[
            # Ülesande 3
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='turniirid',
                column_name='asula',
                points=1,
            ),
            # Ülesande 4
            DataTest(
                title='Kas veergu asula on väärtused sisestatud?',
                name='turniirid',
                column_name='asula',
                points=1,
            ),
            # Ülesande 5
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='turniirid',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
            # Ülesande 6 kontrollid
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='turniirid',
                column_name='toimumiskoht',
                should_exist=False,
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='turniirid',
                column_name='asukoht',
                should_exist=False,
            ),
        ]
    )
]"""