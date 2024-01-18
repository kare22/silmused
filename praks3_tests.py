from silmused.tests.DataTest import DataTest
from silmused.tests.StructureTest import StructureTest
from silmused.tests.ConstraintTest import ConstraintTest
from silmused.tests.FunctionTest import FunctionTest
from silmused.tests.IndexTest import IndexTest
from silmused.tests.ProcedureTest import ProcedureTest
from silmused.tests.TriggerTest import TriggerTest
from silmused.tests.ViewTest import ViewTest

from silmused import TitleLayer, ExecuteLayer

_user1 = 123456
_user2 = 123457
_partii_id = 123123

tests = [
    TitleLayer('Praktikum 3'),
    StructureTest(
        name='turniirid',
        title='Turniiride veerg asukoht',
        column_name='asukoht',
        should_exist=False,
        points=2
    ),
    StructureTest(
        name='partiid',
        title='Partiid veerg vastavus',
        column_name='vastavus',
        points=1,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='un_isikukood',
        constraint_type='UNIQUE',
        points=0.5,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='nimi_unique',
        constraint_type='UNIQUE',
        should_exist=False,
        points=0.25,
    ),
    StructureTest(
        name='klubid',
        column_name='asukoht',
        arguments=['character_maximum_length'],
        expected_value=100,
        points=1,
    ),
    StructureTest(
        name='klubid',
        column_name='asukoht',
        points=1,
    ),
    StructureTest(
        name='v_turniiripartiid'
    ),
    TitleLayer('Kodutöö 6'),
    IndexTest(
        name='ix_riiginimi',
    ),
    IndexTest(
        name='ix_suurus',
    ),
    ConstraintTest(
        name='klubid',
        constraint_type='PRIMARY KEY'
    )
]
