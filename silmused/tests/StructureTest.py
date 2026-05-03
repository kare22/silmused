from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class StructureTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, expected_value=None, expected_type=None,
                 expected_character_maximum_length=None, should_exist=True, where=None,
                 description=None, custom_feedback=None, llm_check=False, debug=None, points=0):

        if column_name is None and expected_type is not None:
            raise Exception('Expected type needs a column to be set!')

        query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.columns WHERE table_name = '{name}'"

        if column_name is not None:
            if isinstance(column_name, str):
                query += f" AND column_name = '{column_name}'"
            elif isinstance(column_name, list):
                for (index, c_name) in enumerate(column_name):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} column_name = '{c_name}'"
                query += ")"
            else:
                raise AttributeError('Parameter column_name must be list or string')

        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_type=expected_type,
            expected_character_maximum_length=expected_character_maximum_length,
            query=query,
            should_exist=should_exist,
            custom_feedback=custom_feedback,
            llm_check=llm_check,
            debug=debug,
        )

        self.column_name = column_name
        self.where = where
        self.test_type = "structure_test"

    def execute(self, cursor):
        if isinstance(self.column_name, list):
            self.query = self._check_separately_for_all_columns(cursor)
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.debug is not None: self.debug_output(result)

        # Result Assessment
        test_type_result = self.result_test_type(result)
        if test_type_result is not None:
            return test_type_result

        if self.expected_value is not None:
            # TODO Is this needed?
            # What is this test checking? result 0,0 is database name, maybe this should check if the value is found in result?
            if self.should_exist:
                # print(self.title, result[0][0])
                return super().response(
                    len(result) != 0 and result[0][0] == self.expected_value,
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_exist_positive_feedback",
                     "params": [self.query]},
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_exist_negative_feedback",
                     "params": [self.query, self.expected_value]},
                )
            else:
                # print(self.title, result[0][0])
                return super().response(
                    len(result) == 0 or result[0][0] != self.expected_value,
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_not_exist_positive_feedback",
                     "params": [self.query]},
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_not_exist_negative_feedback",
                     "params": [self.query, self.expected_value]},
                )
        else:
            if self.should_exist:
                if self.column_name is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": self.test_type,
                         "test_key": "table_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": self.test_type,
                         "test_key": "table_should_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": self.test_type,
                         "test_key": "column_should_exist_positive_feedback",
                         "params": [self.column_name, self.name]},
                        {"test_type": self.test_type,
                         "test_key": "column_should_exist_negative_feedback",
                         "params": [self.column_name, self.name]},
                    )
            else:
                if self.column_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "table_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": self.test_type,
                         "test_key": "table_should_not_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "column_should_not_exist_positive_feedback",
                         "params": [self.column_name, self.name]},
                        {"test_type": self.test_type,
                         "test_key": "column_should_not_exist_negative_feedback",
                         "params": [self.column_name, self.name]},
                    )

    def result_test_type(self, result):
        if self.expected_type is None:
            return None

        type = result[0][7]
        character_maximum_length = result[0][8]
        is_type_correct = True
        is_character_maximum_length_correct = True

        if self.expected_type == 'float':
            if type not in ('float', 'double', 'decimal'):
                is_type_correct = False
        elif self.expected_type == 'integer':
            if type not in ('tinyint', 'smallint', 'mediumint', 'int', 'bigint', 'integer'):
                is_type_correct = False
        elif self.expected_type == 'varchar':
            if type != 'character varying':
                is_type_correct = False
            elif self.expected_character_maximum_length is not None and self.expected_character_maximum_length != character_maximum_length:
                is_character_maximum_length_correct = False
        elif self.expected_type == 'text':
            if type != 'text':
                is_type_correct = False
        elif self.expected_type == 'boolean':
            if type != 'boolean':
                is_type_correct = False

        if is_type_correct is False or is_character_maximum_length_correct is False:
            return super().response(
                False,
                None,
                {"test_type": self.test_type,
                 "test_key": "expected_character_maximum_length_type_check_negative_feedback",
                 "params": [self.expected_character_maximum_length, character_maximum_length, self.name, self.column_name]}
                if is_character_maximum_length_correct is False
                else {"test_type": self.test_type,
                      "test_key": "expected_type_check_negative_feedback",
                      "params": [self.expected_type, type, self.name, self.column_name]},
            )
        return None

    def _check_separately_for_all_columns(self, cursor):
        found = []
        for column in self.column_name:
            query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self.name}' AND column_name = '{column}'"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                found.append(column)
        if len(found) == 0: return self.query
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self.name}'"
        self.column_name = found
        for (index, c_name) in enumerate(self.column_name):
            operator = 'AND (' if index == 0 else 'OR'
            query += f" {operator} column_name = '{c_name}'"
        query += ")"
        return query

    def debug_output(self, result):
        print('STRUCTURE TEST DEBUG: ')
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
            if self.expected_type is not None: print(f"expected_type: {self.expected_type}")
            if self.expected_character_maximum_length is not None: print(f"expected_character_maximum_length: {self.expected_character_maximum_length}")
            if self.column_name_fallback is not None: print(f"column_name_fallback: {self.column_name_fallback}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
            if self.elements is not None: print(f"elements: {self.elements}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.points is not None: print(f"points: {self.points}")
            if self.test_type is not None: print(f"test_type: {self.test_type}")
        if self.debug != 'DEBUG' or self.debug != 'ALL':
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")