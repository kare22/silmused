from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class ProcedureTest(TestDefinition):
    def __init__(self, name, arguments, title=None, description=None, expected_value=None,
                 expected_count=None, number_of_parameters=None, pre_query=None, after_query=None,
                 custom_feedback=None, points=0):
        if after_query is None:
            raise Exception('Parameter "after_query" is required')

        super().__init__(
            name=name,
            title=title,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            pre_query=pre_query,
            query=f"CALL {name}({list_to_string(arguments)})",
            after_query=after_query,
            custom_feedback=custom_feedback
        )

        self.number_of_parameters = number_of_parameters

    def execute(self, cursor):

        # Check that procedure name exists
        test_procedure_exists_result = self.test_procedure_exists(cursor)
        if test_procedure_exists_result is not None:
            return test_procedure_exists_result

        # Check that type is correct
        test_procedure_type_result = self.test_procedure_type(cursor)
        if test_procedure_type_result is not None:
            return test_procedure_type_result

        # Check that procedure number of arguments is correct
        if self.number_of_parameters is not None:
            test_procedure_args_result = self.test_procedure_args(cursor)
            if test_procedure_args_result is not None:
                return test_procedure_args_result

        if self.pre_query is not None:
            cursor.execute(self.pre_query)

        cursor.execute(self.query)

        cursor.execute(self.after_query)

        result = cursor.fetchall()

        if self.expected_count is None:
            if self.custom_feedback is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": "procedure_test",
                     "test_key": "procedure_not_expected_result_count_negative_feedback",
                     "params": [self.name, list_to_string(self.arguments)]},
                    {"test_type": "procedure_test",
                     "test_key": "procedure_not_expected_result_count_negative_feedback",
                     "params": [self.name, list_to_string(self.arguments)]}
                )
            else:
                return super().response(
                    len(result) > 0,
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        else:
            if self.custom_feedback is None:
                return super().response(
                    len(result) == self.expected_count,
                    {"test_type": "procedure_test",
                     "test_key": "procedure_expected_result_count_negative_feedback",
                     "params": [self.expected_count, self.name, list_to_string(self.arguments), len(result)]},
                    {"test_type": "procedure_test",
                     "test_key": "procedure_expected_result_count_negative_feedback",
                     "params": [self.expected_count, self.name, list_to_string(self.arguments), len(result)]}
                )
            else:
                return super().response(
                    len(result) == self.expected_count,
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        # return super().response(
        #    len(result) > 0,
        #    f"Correct count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\"",
        #    f"Expected count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\" but none was found",
        # )

    def test_procedure_exists(self, cursor):
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            if self.custom_feedback is None:
                return super().response(
                    False,
                    {"test_type": "procedure_test",
                     "test_key": "procedure_exists_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "procedure_test",
                     "test_key": "procedure_exists_negative_feedback",
                     "params": [self.name]}
                )
            else:
                return super().response(
                    False,
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None

    def test_procedure_type(self, cursor):
        cursor.execute(
            f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'PROCEDURE' AND routine_name='{self.name}'")
        if not len(cursor.fetchall()) > 0:
            if self.custom_feedback is None:
                return super().response(
                    False,
                    {"test_type": "procedure_test",
                     "test_key": "procedure_type_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "procedure_test",
                     "test_key": "procedure_type_negative_feedback",
                     "params": [self.name]}
                )
            else:
                return super().response(
                    False,
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None

    def test_procedure_args(self, cursor):
        cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        number_of_parameters_result = cursor.fetchall()[0][0]
        if not number_of_parameters_result == self.number_of_parameters:
            if self.custom_feedback is None:
                return super().response(
                    False,
                    {"test_type": "procedure_test",
                     "test_key": "procedure_parameters_exists_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "procedure_test",
                     "test_key": "procedure_parameters_exists_negative_feedback",
                     "params": [self.number_of_parameters, self.name, number_of_parameters_result]}
                )
            else:
                return super().response(
                    False,
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "index_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        return None
