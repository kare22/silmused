from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class ProcedureTest(TestDefinition):
    def __init__(self, name, arguments, title=None, description=None, expected_value=None,
                 expected_count=None, number_of_parameters=None, pre_query=None, after_query=None,
                 should_exist=True, elements=None, custom_feedback=None, llm_check=False, debug=None, points=0):
        query = f"CALL {name}({list_to_string(arguments)})"
        if after_query is None:
            raise Exception('Parameter "after_query" is required')

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
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            pre_query=pre_query,
            query=query,
            after_query=after_query,
            custom_feedback=custom_feedback,
            llm_check=llm_check,
            debug=debug,
        )

        self.number_of_parameters = number_of_parameters
        self.elements = elements
        self.should_exist = should_exist
        self.test_type = "procedure_test"

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

        # Check for required or banned elements
        if isinstance(self.elements, list):
            self.query = self._check_separately_for_all_elements(cursor)

        cursor.execute(self.query)
        cursor.execute(self.after_query)
        result = cursor.fetchall()
        if self.debug is not None: self.debug_output(result)

        if self.elements is not None:
            if self.should_exist:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "procedure_required_elements_positive_feedback",
                     "params": [self.elements, self.name]},
                    {"test_type": self.test_type,
                     "test_key": "procedure_required_elements_negative_feedback",
                     "params": [self.elements, self.name]},
                )
            else:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "procedure_banned_elements_positive_feedback",
                     "params": [self.elements, self.name]},
                    {"test_type": self.test_type,
                     "test_key": "procedure_banned_elements_negative_feedback",
                     "params": [self.elements, self.name]},
                )
        elif self.expected_count is None:
            return super().response(
                len(result) > 0,
                {"test_type": self.test_type,
                 "test_key": "procedure_not_expected_result_count_negative_feedback",
                 "params": [self.name, list_to_string(self.arguments)]},
                {"test_type": self.test_type,
                 "test_key": "procedure_not_expected_result_count_negative_feedback",
                 "params": [self.name, list_to_string(self.arguments)]}
            )
        else:
            return super().response(
                len(result) == self.expected_count,
                {"test_type": self.test_type,
                 "test_key": "procedure_expected_result_count_negative_feedback",
                 "params": [self.expected_count, self.name, list_to_string(self.arguments), len(result)]},
                {"test_type": self.test_type,
                 "test_key": "procedure_expected_result_count_negative_feedback",
                 "params": [self.expected_count, self.name, list_to_string(self.arguments), len(result)]}
            )
        # return super().response(
        #    len(result) > 0,
        #    f"Correct count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\"",
        #    f"Expected count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\" but none was found",
        # )

    def test_procedure_exists(self, cursor):
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                {"test_type": self.test_type,
                 "test_key": "procedure_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
                 "test_key": "procedure_exists_negative_feedback",
                 "params": [self.name]}
            )
        return None

    def test_procedure_type(self, cursor):
        cursor.execute(
            f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'PROCEDURE' AND routine_name='{self.name}'")
        if not len(cursor.fetchall()) > 0:
            return super().response(
                False,
                {"test_type": self.test_type,
                 "test_key": "procedure_type_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
                 "test_key": "procedure_type_negative_feedback",
                 "params": [self.name]}
            )
        return None

    def test_procedure_args(self, cursor):
        cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        number_of_parameters_result = cursor.fetchall()[0][0]
        if not number_of_parameters_result == self.number_of_parameters:
            return super().response(
                False,
                {"test_type": self.test_type,
                 "test_key": "procedure_parameters_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
                 "test_key": "procedure_parameters_exists_negative_feedback",
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
        print('PROCEDURE TEST DEBUG: ')
        if self.debug == 'DEBUG':
            if self.title is not None: print(f"Test title: {self.title}")
            print(f"query: {self.query}")
            print(f"result: {result}")
        if self.debug == 'ALL':
            if self.name is not None: print(f"name: {self.name}")
            if self.arguments is not None: print(f"arguments: {self.arguments}")
            if self.description is not None: print(f"description: {self.description}")
            if self.expected_value is not None: print(f"expected_value: {self.expected_value}")
            if self.expected_count is not None: print(f"expected_count: {self.expected_count}")
            if self.number_of_parameters is not None: print(f"number_of_parameters: {self.number_of_parameters}")
            if self.pre_query is not None: print(f"pre_query: {self.pre_query}")
            if self.after_query is not None: print(f"after_query: {self.after_query}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
            if self.elements is not None: print(f"elements: {self.elements}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.points is not None: print(f"points: {self.points}")
            if self.test_type is not None: print(f"test_type: {self.test_type}")
        if self.debug != 'DEBUG' or self.debug != 'ALL':
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")