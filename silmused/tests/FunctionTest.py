from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class FunctionTest(TestDefinition):
    def __init__(self, name, title=None, arguments=None, column_name=None, where=None, description=None, expected_value=None,
                 expected_count=None, number_of_parameters=None, custom_feedback=None, points=0):
        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            custom_feedback=custom_feedback,
            query=f"SELECT {column_name if column_name is not None else '*'} FROM {name}({list_to_string(arguments if arguments is not None else '')})"  # TODO implement parameters,
        )
        if isinstance(expected_value, list):
            self.expected_value_list = True
            if isinstance(expected_value[0], str):
                self.expected_value_group = "strings"
            else:
                self.expected_value_group = "numbers"
                min_value = None
                max_value = None
                for value in expected_value:
                    if isinstance(value, str):
                        raise Exception('Ranged expected value cannot be a string')
                    if min_value is None:
                        min_value = value
                    elif value < min_value:
                        min_value = value
                    if max_value is None:
                        max_value = value
                    elif value > max_value:
                        max_value = value
                self.expected_min_value = min_value
                self.expected_max_value = max_value
        elif isinstance(expected_count, list):
            self.expected_value_list = True
            if isinstance(expected_count[0], str):
                self.expected_value_group = "strings"
            else:
                self.expected_value_group = "numbers"
                min_value = None
                max_value = None
                for value in expected_count:
                    if isinstance(value, str):
                        raise Exception('Ranged expected value cannot be a string')
                    if min_value is None:
                        min_value = value
                    elif value < min_value:
                        min_value = value
                    if max_value is None:
                        max_value = value
                    elif value > max_value:
                        max_value = value
                self.expected_min_value = min_value
                self.expected_max_value = max_value
        else:
            self.expected_value_list = False
            self.expected_value_group = "nothing"

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
                if self.custom_feedback is None:
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
                        len(result) > 0,
                        {"test_type": "function_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "function_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.expected_value_group == "numbers":
                    if self.custom_feedback is None:
                        return super().response(
                            self.expected_min_value <= len(result) <= self.expected_max_value,
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_numbers_positive_feedback",
                             "params": [len(result), self.expected_min_value, self.expected_max_value]},
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_numbers_negative_feedback",
                             "params": [len(result), self.expected_min_value, self.expected_max_value]},
                        )
                    else:
                        return super().response(
                            self.expected_min_value <= len(result) <= self.expected_max_value,
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
                elif self.expected_value_group == "strings":
                    if self.custom_feedback is None:
                        return super().response(
                            result[0][0] in self.expected_value,
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_strings_positive_feedback",
                             "params": [str(result[0][0]), self.expected_value]},
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_strings_negative_feedback",
                             "params": [str(result[0][0]), self.expected_value]},
                        )
                    else:
                        return super().response(
                            result[0][0] in self.expected_value,
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
                if self.custom_feedback is None:
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
                    return super().response(
                        len(result) == self.expected_count,
                        {"test_type": "function_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "function_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
        else:
            # TODO when type is decimal but we give float, we get an error
            # if type(result[0][0]) != type(self.expected_value):
            #     return super().response(
            #         False,
            #         'Correct',
            #         f"Expected type {type(self.expected_value)} but got {type(result[0][0])}",
            #     )
            if self.expected_value_list:
                if self.expected_value_group == "numbers":
                    if self.custom_feedback is None:
                        return super().response(
                            self.expected_min_value <= result[0][0] <= self.expected_max_value,
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_numbers_positive_feedback",
                             "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value]},
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_numbers_negative_feedback",
                             "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value]},
                        )
                    else:
                        return super().response(
                            self.expected_min_value <= result[0][0] <= self.expected_max_value,
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
                elif self.expected_value_group == "strings":
                    if self.custom_feedback is None:
                        return super().response(
                            result[0][0] in self.expected_value,
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_strings_positive_feedback",
                             "params": [str(result[0][0]), self.expected_value]},
                            {"test_type": "function_test",
                             "test_key": "function_expected_value_group_strings_negative_feedback",
                             "params": [str(result[0][0]), self.expected_value]},
                        )
                    else:
                        return super().response(
                            result[0][0] in self.expected_value,
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "function_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
            if self.custom_feedback is None:
                return super().response(
                    str(result[0][0]) == str(self.expected_value),
                    {"test_type": "function_test",
                     "test_key": "function_expected_value_positive_feedback",
                     "params": [self.expected_value]},
                    {"test_type": "function_test",
                     "test_key": "function_expected_value_negative_feedback",
                     "params": [self.expected_value, result[0][0]]}
                )
            else:
                return super().response(
                    str(result[0][0]) == str(self.expected_value),
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )

    def test_function_exists(self, cursor):
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            if self.custom_feedback is None:
                return super().response(
                    False,
                    {"test_type": "function_test",
                     "test_key": "function_exists_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "function_test",
                     "test_key": "function_exists_negative_feedback",
                     "params": [self.name]}
                )
            else:
                return super().response(
                    False,
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None

    def test_function_type(self, cursor):
        cursor.execute(
            f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION' AND routine_name='{self.name}'")
        if not len(cursor.fetchall()) > 0:
            if self.custom_feedback is None:
                return super().response(
                    False,
                    {"test_type": "function_test",
                     "test_key": "function_type_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "function_test",
                     "test_key": "function_type_negative_feedback",
                     "params": [self.name]}
                )
            else:
                return super().response(
                    False,
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None

    def test_function_args(self, cursor):
        cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        number_of_parameters_result = cursor.fetchall()[0][0]
        if not number_of_parameters_result == self.number_of_parameters:
            if self.custom_feedback is None:
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
            else:
                return super().response(
                    False,
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "function_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None
