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
    ChecksLayer(
        title='ConstraintTest feedback tests',
        tests=[
            ConstraintTest(
                title='table_constraint_should_exist_negative_feedback',
                name='riigid2',
            ),
            ConstraintTest(
                title='table_column_constraint_should_exist_negative_feedback',
                name='asulad',
                column_name='id',
            ),
            ConstraintTest(
                title='table_column_constraint_name_should_exist_negative_feedback',
                name='asulad',
                column_name='id',
                constraint_name='un1_isikukood',
            ),
            ConstraintTest(
                title='table_column_constraint_type_should_exist_negative_feedback',
                name='asulad',
                column_name='id',
                constraint_type='UNIQUE',
            ),
            ConstraintTest(
                title='table_column_constraint_name_and_type_should_exist_negative_feedback',
                name='asulad',
                column_name='id',
                constraint_name='un1_isikukood',
                constraint_type='UNIQUE',
            ),
            ConstraintTest(
                title='table_constraint_should_not_exist_negative_feedback',
                name='riigid',
                should_exist=False,
            ),
            ConstraintTest(
                title='table_column_constraint_should_not_exist_negative_feedback',
                name='asulad',
                column_name='nimi',
                should_exist=False,
            ),
            ConstraintTest(
                title='table_column_constraint_name_should_not_exist_negative_feedback',
                name='isikud',
                column_name='isikukood',
                constraint_name='un_isikukood',
                should_exist=False,
            ),
            ConstraintTest(
                title='table_column_constraint_type_should_not_exist_negative_feedback',
                name='isikud',
                column_name='isikukood',
                constraint_type='UNIQUE',
                should_exist=False,
            ),
            ConstraintTest(
                title='table_column_constraint_name_and_type_should_not_exist_negative_feedback',
                name='isikud',
                column_name='isikukood',
                constraint_name='un_isikukood',
                constraint_type='UNIQUE',
                should_exist=False,
            ),
        ]
    )
]
"""
ChecksLayer(
        title='StructureTest feedback tests',
        tests=[
            # Structure tests that seem pointless
            # expected_value_should_exist_negative_feedback
            StructureTest(
                title='expected_value_should_exist_negative_feedback',
                name='isikud',
                expected_value=80,
            ),
    
            # expected_value_should_not_exist_negative_feedback
            StructureTest(
                title='expected_value_should_not_exist_negative_feedback',
                name='asulad',
                column_name='nimi',
                expected_value='Pärnu',
                should_exist=False
            ),
            # Good tests
            # table_should_exist_negative_feedback
            StructureTest(
                title='table_should_exist_negative_feedback',
                name='isikud2',
            ),
            # column_should_exist_negative_feedback
            StructureTest(
                title='column_should_exist_negative_feedback',
                name='isikud',
                column_name='idd',
            ),

            # table_should_not_exist_negative_feedback
            StructureTest(
                title='table_should_not_exist_negative_feedback',
                name='isikud',
                should_exist=False,
            ),

            # column_should_not_exist_negative_feedback
            StructureTest(
                title='column_should_not_exist_negative_feedback',
                name='isikud',
                column_name='id',
                should_exist=False,
            ),

        ]
    ),
"""

