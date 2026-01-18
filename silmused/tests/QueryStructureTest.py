from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class QueryStructureTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, should_exist=True, where=None,
                 description=None, custom_feedback=None, banned_arguments=None, points=0):

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
        if banned_arguments is not None:
            query = "SELECT * FROM information_schema.views WHERE table_name = 'query_view'"
            if isinstance(banned_arguments, str):
                query += f" AND view_definition ILIKE '%{banned_arguments}%'"
            elif isinstance(banned_arguments, list):
                for (index, arg) in enumerate(banned_arguments):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} view_definition ILIKE '%{arg}%'"
                query += ")"
            else:
                raise AttributeError('Parameter banned_arguments must be list or string')

        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            query=query,
            should_exist=should_exist,
            custom_feedback=custom_feedback,
            banned_arguments=banned_arguments,
        )

        self.column_name = column_name
        self.where = where

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.banned_arguments is not None:
            if self.custom_feedback is None:
                return super().response(
                    len(result) == 0,
                    {"test_type": "query_structure_test",
                     "test_key": "query_banned_arguments_positive_feedback",
                     "params": [self.banned_arguments]},
                    {"test_type": "query_structure_test",
                     "test_key": "query_banned_arguments_negative_feedback",
                     "params": [self.banned_arguments]},
                )
            else:
                return super().response(
                    len(result) == 0,
                    {"test_type": "query_structure_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                    {"test_type": "query_structure_test",
                     "test_key": "custom_feedback",
                     "params": [self.custom_feedback]},
                )
        elif self.should_exist:
            if self.column_name is None:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_table_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_table_should_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_column_should_exist_positive_feedback",
                         "params": [self.column_name]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_column_should_exist_negative_feedback",
                         "params": [self.column_name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
        else:
            if self.column_name is None:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_table_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_table_should_not_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_column_should_not_exist_positive_feedback",
                         "params": [self.column_name]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_column_should_not_exist_negative_feedback",
                         "params": [self.column_name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "query_structure_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
