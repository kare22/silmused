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
    # Kodutöö 4 kontrollid
    ChecksLayer(
        title='Vaate v_keskminepartii kontrollid',
        tests=[
            DataTest(
                title='Kas turniiril Plekkkarikas 2010 keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 3)',
                where="turniiri_nimi = 'Plekkkarikas 2010'",
                expected_value=[23.764,24.27],
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas turniiril Kolme klubi kohtumine keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 2)',
                where="turniiri_nimi = 'Kolme klubi kohtumine'",
                expected_value=[23.03,23.7],
                isView=True,
                points=1,
            ),
        ]
    ),
]