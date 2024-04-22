from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class FunctionTest(TestDefinition):
    def __init__(self, name, title=None, arguments=None, column_name=None, where=None, description=None, expected_value=None,
                 expected_count=None, number_of_parameters=None, points=0):
        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            query=f"SELECT {column_name if column_name is not None else '*'} FROM {name}({list_to_string(arguments if arguments is not None else '')})"  # TODO implement parameters,
        )

        self.number_of_parameters = number_of_parameters

    def execute(self, cursor):

        # Check that function name exists
        test_function_exists_result = self.test_function_exists(cursor)
        if test_function_exists_result is not None:
            return test_function_exists_result

        # Check that type is correct
        test_function_type_result = self.test_function_type(cursor)
        if test_function_type_result is not None:
            return test_function_type_result

        # Check that function number of arguments is correct
        if self.number_of_parameters is not None:
            test_function_args_result = self.test_function_args(cursor)
            if test_function_args_result is not None:
                return test_function_args_result

        # TODO Add a test to check output arguments
        # cursor.execute("SELECT proargnames FROM pg_catalog.pg_proc WHERE proname='f_voit_viik_kaotus'")
        # test_tesult = cursor.fetchall()[0][0]
        # print(len(test_tesult)-(self.number_of_parameters if self.number_of_parameters is not None else 0))

        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.expected_value is None:
            if self.expected_count is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": "function_test",
                     "test_key": "function_not_expected_value_not_expected_result_count_positive_feedback",
                     "params": [self.name, list_to_string(self.arguments)]},
                    {"test_type": "function_test",
                     "test_key": "function_not_expected_value_not_expected_result_count_negative_feedback",
                     "params": [self.name, list_to_string(self.arguments)]}
                )
            else:
                return super().response(
                    len(result) == self.expected_count,
                    {"test_type": "function_test",
                     "test_key": "function_not_expected_value_expected_result_count_positive_feedback",
                     "params": [self.expected_count, self.name, list_to_string(self.arguments)]},
                    {"test_type": "function_test",
                     "test_key": "function_not_expected_value_expected_result_count_negative_feedback",
                     "params": [self.expected_count, self.name, list_to_string(self.arguments), len(result)]}
                )
        else:
            # TODO when type is decimal but we give float, we get an error
            # if type(result[0][0]) != type(self.expected_value):
            #     return super().response(
            #         False,
            #         'Correct',
            #         f"Expected type {type(self.expected_value)} but got {type(result[0][0])}",
            #     )
            return super().response(
                str(result[0][0]) == str(self.expected_value),
                {"test_type": "function_test",
                 "test_key": "function_expected_value_positive_feedback",
                 "params": [self.expected_value]},
                {"test_type": "function_test",
                 "test_key": "function_expected_value_negative_feedback",
                 "params": [self.expected_value, result[0][0]]}
            )

    def test_function_exists(self, cursor):
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                {"test_type": "function_test",
                 "test_key": "function_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": "function_test",
                 "test_key": "function_exists_negative_feedback",
                 "params": [self.name]}
            )
        return None

    def test_function_type(self, cursor):
        cursor.execute(
            f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION' AND routine_name='{self.name}'")
        if not len(cursor.fetchall()) > 0:
            return super().response(
                False,
                {"test_type": "function_test",
                 "test_key": "function_type_positive_feedback",
                 "params": [self.name]},
                {"test_type": "function_test",
                 "test_key": "function_type_negative_feedback",
                 "params": [self.name]}
            )
        return None

    def test_function_args(self, cursor):
        cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        number_of_parameters_result = cursor.fetchall()[0][0]
        if not number_of_parameters_result == self.number_of_parameters:
            return super().response(
                False,
                {"test_type": "function_test",
                 "test_key": "function_parameters_amount_positive_feedback",
                 "params": [self.name]}
                ,
                {"test_type": "function_test",
                 "test_key": "function_parameters_amount_negative_feedback",
                 "params": [self.number_of_parameters, self.name, number_of_parameters_result]}
            )
        return None
