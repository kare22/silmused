from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class FunctionTest(TestDefinition):
    def __init__(self, name, title=None, arguments=None, column_name=None, where=None, description=None,
                 expected_value=None, expected_count=None, expected_value_query=None, number_of_parameters=None,
                 should_exist=True, elements=None, custom_feedback=None, llm_check=False, debug=None, points=0):

        query = f"SELECT {column_name if column_name is not None else '*'} FROM {name}({list_to_string(arguments if arguments is not None else '')})"

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

        if elements is not None:
            query = f"SELECT * FROM pg_proc WHERE proname = '{name}'"
            if isinstance(elements, str):
                query += f" AND prosrc ILIKE '%{elements}%'"
            elif isinstance(elements, list):
                for (index, arg) in enumerate(elements):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} prosrc ILIKE '%{arg}%'"
                query += ")"
            else:
                raise AttributeError('Parameter elements must be list or string')

        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            query=query,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            custom_feedback=custom_feedback,
            llm_check=llm_check,
            debug=debug,
            # TODO implement parameters,
        )

        self.number_of_parameters = number_of_parameters
        self.expected_value_query = expected_value_query
        self.elements = elements
        self.should_exist = should_exist
        self.test_type = "function_test"

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

        if self.expected_value_query is not None:
            cursor.execute(self.expected_value_query)
            result = cursor.fetchall()
            self.expected_value = result[0][0]

        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.debug is not None: self.debug_output(result)

        # Result assessment
        if self.elements is not None:
            if self.should_exist:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "function_required_elements_positive_feedback",
                     "params": [self.elements, self.name]},
                    {"test_type": self.test_type,
                     "test_key": "function_required_elements_negative_feedback",
                     "params": [self.elements, self.name]},
                )
            else:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "function_banned_elements_positive_feedback",
                     "params": [self.elements, self.name]},
                    {"test_type": self.test_type,
                     "test_key": "function_banned_elements_negative_feedback",
                     "params": [self.elements, self.name]},
                )
        elif self.expected_value is None:
            if self.expected_count is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "function_not_expected_value_not_expected_result_count_positive_feedback",
                     "params": [self.name, list_to_string(self.arguments)]},
                    {"test_type": self.test_type,
                     "test_key": "function_not_expected_value_not_expected_result_count_negative_feedback",
                     "params": [self.name, list_to_string(self.arguments)]}
                )
            else:
                if self.expected_value_group == "numbers":
                    return super().response(
                        self.expected_min_value <= len(result) <= self.expected_max_value,
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_numbers_positive_feedback",
                         "params": [len(result), self.expected_min_value, self.expected_max_value]},
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_numbers_negative_feedback",
                         "params": [len(result), self.expected_min_value, self.expected_max_value]},
                    )
                elif self.expected_value_group == "strings":
                    return super().response(
                        result[0][0] in self.expected_value,
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_strings_positive_feedback",
                         "params": [str(result[0][0]), self.expected_value]},
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_strings_negative_feedback",
                         "params": [str(result[0][0]), self.expected_value]},
                    )
                return super().response(
                    len(result) == self.expected_count,
                    {"test_type": self.test_type,
                     "test_key": "function_not_expected_value_expected_result_count_positive_feedback",
                     "params": [self.expected_count, self.name, list_to_string(self.arguments)]},
                    {"test_type": self.test_type,
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
            if self.expected_value_list:
                if self.expected_value_group == "numbers":
                    return super().response(
                        self.expected_min_value <= result[0][0] <= self.expected_max_value,
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_numbers_positive_feedback",
                         "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value]},
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_numbers_negative_feedback",
                         "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value]},
                    )
                elif self.expected_value_group == "strings":
                    return super().response(
                        result[0][0] in self.expected_value,
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_strings_positive_feedback",
                         "params": [str(result[0][0]), self.expected_value]},
                        {"test_type": self.test_type,
                         "test_key": "function_expected_value_group_strings_negative_feedback",
                         "params": [str(result[0][0]), self.expected_value]},
                    )
            if not isinstance(result[0][0], str) and not isinstance(self.expected_value, str):
                return super().response(
                    result[0][0] == self.expected_value,
                    {"test_type": self.test_type,
                     "test_key": "function_expected_value_positive_feedback",
                     "params": [self.expected_value]},
                    {"test_type": self.test_type,
                     "test_key": "function_expected_value_negative_feedback",
                     "params": [self.expected_value, result[0][0]]}
                )
            else:
                return super().response(
                    str(result[0][0]) == str(self.expected_value),
                    {"test_type": self.test_type,
                     "test_key": "function_expected_value_positive_feedback",
                     "params": [self.expected_value]},
                    {"test_type": self.test_type,
                     "test_key": "function_expected_value_negative_feedback",
                     "params": [self.expected_value, result[0][0]]}
                )

    def test_function_exists(self, cursor):
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                {"test_type": self.test_type,
                 "test_key": "function_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
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
                {"test_type": self.test_type,
                 "test_key": "function_type_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
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
                {"test_type": self.test_type,
                 "test_key": "function_parameters_amount_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
                 "test_key": "function_parameters_amount_negative_feedback",
                 "params": [self.number_of_parameters, self.name, number_of_parameters_result]}
            )
        return None

    def _check_separately_for_all_elements(self, cursor):
        found = []
        for element in self.elements:
            query = f"SELECT * FROM pg_proc WHERE proname = '{self.name}' AND prosrc ILIKE '%{element}%'"
            cursor.execute(query)
            result = cursor.fetchall()
            if self.should_exist and len(result) == 0:
                found.append(element)
            elif not self.should_exist and len(result) > 0:
                found.append(element)
        if len(found) == 0: return self.query
        query = f"SELECT * FROM pg_proc WHERE proname = '{self.name}'"
        self.elements = found
        for (index, arg) in enumerate(self.elements):
            operator = 'AND (' if index == 0 else 'OR'
            query += f" {operator} prosrc ILIKE '%{arg}%'"
        query += ")"
        return query

    def debug_output(self, result):
        print('FUNCTION TEST DEBUG: ')
        if self.debug == 'DEBUG':
            if self.title is not None: print(f"Test title: {self.title}")
            print(f"query: {self.query}")
            print(f"result: {result}")
        if self.debug == 'ALL':
            if self.name is not None: print(f"name: {self.name}")
            if self.arguments is not None: print(f"arguments: {self.arguments}")
            if self.column_name is not None: print(f"column_name: {self.column_name}")
            if self.where is not None: print(f"where: {self.where}")
            if self.description is not None: print(f"description: {self.description}")
            if self.expected_value is not None: print(f"expected_value: {self.expected_value}")
            if self.expected_count is not None: print(f"expected_count: {self.expected_count}")
            if self.expected_value_query is not None: print(f"expected_value_query: {self.expected_value_query}")
            if self.number_of_parameters is not None: print(f"number_of_parameters: {self.number_of_parameters}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
            if self.elements is not None: print(f"elements: {self.elements}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.points is not None: print(f"points: {self.points}")
            if self.expected_value_list is not None: print(f"expected_value_list: {self.expected_value_list}")
            if self.expected_value_group is not None: print(f"expected_value_group: {self.expected_value_group}")
            if self.expected_min_value is not None: print(f"expected_min_value: {self.expected_min_value}")
            if self.expected_max_value is not None: print(f"expected_max_value: {self.expected_max_value}")
            if self.test_type is not None: print(f"test_type: {self.test_type}")
        if self.debug != 'DEBUG' or self.debug != 'ALL':
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")