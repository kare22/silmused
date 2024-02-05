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
"""
# Praktikum 3
tests = [
    ChecksLayer(
        title='',
        tests=[
            
        ],
    )
]
# Praktikum 4
"""
tests = [
    # Ülesanne 1, 4
    ChecksLayer(
        title='Tabeli Asulad kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel asulad on olemas?',
                name='asulad',
                points=1,
            ),
            StructureTest(
                title='Kas veerg id on olemas?',
                name='asulad',
                column_name='id'
            ),
            StructureTest(
                title='Kas veerg nimi on olemas?',
                name='asulad',
                column_name='nimi'
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='asulad',
                constraint_type='PRIMARY KEY',
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='asulad',
                constraint_type='UNIQUE',
            ),
            # Ülesanne 4
            DataTest(
                title='Kas tabelis asulad on andmed olemas?',
                name='asulad'
            ),
        ]
    ),
    # Ülesanne 2, 3
    ChecksLayer(
        title='Tabeli Riigid kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel riigid on olemas?',
                name='riigid',
            ),
            StructureTest(
                title='Kas veerg id on olemas?',
                name='riigid',
                column_name='id'
            ),
            StructureTest(
                title='Kas veerg nimi on olemas?',
                name='riigid',
                column_name='nimi'
            ),
            StructureTest(
                title='Kas veerg pealinn on olemas?',
                name='riigid',
                column_name='pealinn'
            ),
            StructureTest(
                title='Kas veerg rahvaarv on olemas?',
                name='riigid',
                column_name='rahvaarv'
            ),
            StructureTest(
                title='Kas veerg pindala on olemas?',
                name='riigid',
                column_name='pindala'
            ),
            StructureTest(
                title='Kas veerg skp_mld on olemas?',
                name='riigid',
                column_name='skp_mld'
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='asulad',
                constraint_type='PRIMARY KEY',
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='asulad',
                constraint_type='UNIQUE',
            ),
            DataTest(
                title='Kas tabelis riigid on andmed olemas?',
                name='riigid'
            ),
        ]
    ),
    # Ülesanne 5, 6, 7, 9
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
            ),
            DataTest(
                title='Kas veerus asula on andmed olemas?',
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
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='klubid',
                constraint_type='FOREIGN KEY',
            ),

        ]
    ),
]