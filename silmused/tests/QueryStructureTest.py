from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class QueryStructureTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, should_exist=True, where=None,
                 description=None, custom_feedback=None, elements=None, llm_check=False, points=0):

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

        if elements is not None:
            query = "SELECT * FROM information_schema.views WHERE table_name = 'query_view'"
            if isinstance(elements, str):
                query += f" AND view_definition ILIKE '%{elements}%'"
            elif isinstance(elements, list):
                for (index, arg) in enumerate(elements):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} view_definition ILIKE '%{arg}%'"
                query += ")"
            else:
                raise AttributeError('Parameter elements must be a list or string')

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
            elements=elements,
            llm_check=llm_check,
        )

        self.column_name = column_name
        self.where = where

    def execute(self, cursor):
        if isinstance(self.elements, list):
            self.query = self._check_separately_for_all_elements(cursor)
        if isinstance(self.column_name, list):
            self.query = self._check_separately_for_all_columns(cursor)
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.elements is not None:
            # TODO if in the future there is a requirement to count specific amount of elements used, then this can be used
            # select (CHAR_LENGTH(lower(view_definition)) - CHAR_LENGTH(REPLACE(lower(view_definition), lower('maletäht'), ''))) / CHAR_LENGTH(lower('maletäht')) as alamparing from information_schema.views where table_name = 'query_view';
            if self.should_exist:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_required_elements_positive_feedback",
                         "params": [self.elements]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_required_elements_negative_feedback",
                         "params": [self.elements]},
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
                        len(result) == 0,
                        {"test_type": "query_structure_test",
                         "test_key": "query_banned_elements_positive_feedback",
                         "params": [self.elements]},
                        {"test_type": "query_structure_test",
                         "test_key": "query_banned_elements_negative_feedback",
                         "params": [self.elements]},
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

    def _check_separately_for_all_elements(self, cursor):
        found = []
        for element in self.elements:
            query = f"SELECT * FROM information_schema.views WHERE table_name = 'query_view' AND view_definition ILIKE '%{element}%'"
            cursor.execute(query)
            result = cursor.fetchall()
            if self.should_exist and len(result) == 0:
                found.append(element)
            elif not self.should_exist and len(result) > 0:
                found.append(element)
        if len(found) == 0: return self.query
        query = f"SELECT * FROM information_schema.views WHERE table_name = 'query_view'"
        self.elements = found
        for (index, arg) in enumerate(self.elements):
            operator = 'AND (' if index == 0 else 'OR'
            query += f" {operator} view_definition ILIKE '%{arg}%'"
        query += ")"
        return query

    def _check_separately_for_all_columns(self, cursor):
        found = []
        for column in self.column_name:
            query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self.name}' AND column_name = '{column}'"
            cursor.execute(query)
            result = cursor.fetchall()
            if self.should_exist and len(result) == 0:
                found.append(column)
            elif not self.should_exist and len(result) > 0:
                found.append(column)
        if len(found) == 0: return self.query
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{self.name}'"
        self.column_name = found
        for (index, c_name) in enumerate(self.column_name):
            operator = 'AND (' if index == 0 else 'OR'
            query += f" {operator} column_name = '{c_name}'"
        query += ")"
        return query
