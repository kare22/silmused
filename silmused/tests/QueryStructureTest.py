from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class QueryStructureTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, expected_value=None, expected_type=None, expected_character_maximum_length=None, should_exist=True, where=None, description=None, points=0):
        if column_name is None and expected_type is not None:
            raise Exception('Expected type needs a column to be set!')

        query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.columns WHERE table_name = '{name}'"

        if column_name is not None:
            if type(column_name) == str:
                query += f" AND column_name = '{column_name}'"
            elif type(column_name) == list:
                for (index, name) in enumerate(column_name):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} column_name = '{name}'"
            else:
                raise AttributeError('Parameter column_name must be list or string')
        if type(column_name) == list:
            query += ")"
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
        )

        self.column_name = column_name
        self.where = where

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        test_type_result = self.test_type(result)
        if test_type_result is not None:
            return test_type_result

        if self.expected_value is not None:
            # TODO Is this needed?
            # What is this test checking? result 0,0 is database name, maybe this should check if the value is found in result?
            if self.should_exist:
                # print(self.title, result[0][0])
                return super().response(
                    len(result) != 0 and result[0][0] == self.expected_value,
                    {"test_type": "structure_test",
                     "test_key": "expected_value_should_exist_positive_feedback",
                     "params": [self.query]},
                    {"test_type": "structure_test",
                     "test_key": "expected_value_should_exist_negative_feedback",
                     "params": [self.query, self.expected_value]},
                )
            else:
                # print(self.title, result[0][0])
                return super().response(
                    len(result) == 0 or result[0][0] != self.expected_value,
                    {"test_type": "structure_test",
                     "test_key": "expected_value_should_not_exist_positive_feedback",
                     "params": [self.query]},
                    {"test_type": "structure_test",
                     "test_key": "expected_value_should_not_exist_negative_feedback",
                     "params": [self.query, self.expected_value]},
                )
        else:
            if self.should_exist:
                if self.column_name is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "structure_test",
                         "test_key": "table_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "structure_test",
                         "test_key": "table_should_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "structure_test",
                         "test_key": "column_should_exist_positive_feedback",
                         "params": [self.column_name, self.name]},
                        {"test_type": "structure_test",
                         "test_key": "column_should_exist_negative_feedback",
                         "params": [self.column_name, self.name]},
                    )
            else:
                if self.column_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "structure_test",
                         "test_key": "table_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "structure_test",
                         "test_key": "table_should_not_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "structure_test",
                         "test_key": "column_should_not_exist_positive_feedback",
                         "params": [self.column_name, self.name]},
                        {"test_type": "structure_test",
                         "test_key": "column_should_not_exist_negative_feedback",
                         "params": [self.column_name, self.name]},
                    )