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

_user1 = 123456
_user2 = 123457
_partii_id = 123123
_asula_id = 200
_asula_nimi = 'Test_asula'
_klubi_id = 201
_klubi_nimi = 'Klubi kustutamiseks'

tests = [
    ChecksLayer(
        title='Single test',
        tests=[
            # 8
            DataTest(
                title='Kas isiku Irys perenimi on muudetud?',
                name='isikud',
                column_name='perenimi',
                where="eesnimi = 'Irys'",
                expected_value='Kompvek1',
                custom_feedback="test test",
                points=3,
            ),
        ],
    ),
]