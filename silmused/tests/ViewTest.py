from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class ViewTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, expected_value=None, should_exist=True,
                 where=None, description=None, custom_feedback=None, isMaterialized=False, elements=None,
                 llm_check=False, points=0):
        if isMaterialized:
            query = f"SELECT * FROM pg_matviews WHERE matviewname = '{name}'"
        else:
            query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.columns WHERE table_name = '{name}'"

        if column_name is not None:
            if type(column_name) == str:
                query += f" AND column_name = '{column_name}'"
            elif type(column_name) == list:
                for (index, name) in enumerate(column_name):
                    operator = 'AND' if index == 0 else 'OR'
                    query += f" {operator} column_name = '{name}'"
            else:
                raise AttributeError('Parameter column_name must be list or string')

        if elements is not None:
            if not isMaterialized:
                query = f"SELECT * FROM pg_views WHERE viewname = '{name}'"
            if isinstance(elements, str):
                query += f" AND definition ILIKE '%{elements}%'"
            elif isinstance(elements, list):
                for (index, arg) in enumerate(elements):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} definition ILIKE '%{arg}%'"
                query += ")"
            else:
                raise AttributeError('Parameter elements must be list or string')

        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            expected_value=expected_value,
            description=description,
            query=query,
            should_exist=should_exist,
            custom_feedback=custom_feedback,
            elements=elements,
            llm_check=llm_check,
        )

        self.column_name = column_name
        self.where = where
        self.isMaterialized = isMaterialized
        self.test_type = "view_test"

    def execute(self, cursor):
        if isinstance(self.elements, list):
            self.query = self._check_separately_for_all_elements(cursor)
        if isinstance(self.column_name, list):
            self.query = self._check_separately_for_all_columns(cursor)
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.isMaterialized:
            if self.elements is not None:
                if self.should_exist:
                    return super().response(
                        len(result) > 0,
                        {"test_type": self.test_type,
                         "test_key": "mat_view_required_elements_positive_feedback",
                         "params": [self.elements,self.name]},
                        {"test_type": self.test_type,
                         "test_key": "mat_view_required_elements_negative_feedback",
                         "params": [self.elements,self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "mat_view_banned_elements_positive_feedback",
                         "params": [self.elements,self.name]},
                        {"test_type": self.test_type,
                         "test_key": "mat_view_banned_elements_negative_feedback",
                         "params": [self.elements,self.name]},
                    )
            elif self.should_exist:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "mat_view_should_exist_positive_feedback",
                     "params": [self.name]},
                    {"test_type": self.test_type,
                     "test_key": "mat_view_should_exist_negative_feedback",
                     "params": [self.name]},
                )
            else:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "mat_view_should_not_exist_positive_feedback",
                     "params": [self.name]},
                    {"test_type": self.test_type,
                     "test_key": "mat_view_should_not_exist_negative_feedback",
                     "params": [self.name]},
                )
        if self.elements is not None:
            if self.should_exist:
                return super().response(
                    len(result) > 0,
                        {"test_type": self.test_type,
                         "test_key": "view_required_elements_positive_feedback",
                         "params": [self.elements,self.name]},
                        {"test_type": self.test_type,
                         "test_key": "view_required_elements_negative_feedback",
                         "params": [self.elements,self.name]},
                )
            else:
                return super().response(
                    len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "view_banned_elements_positive_feedback",
                         "params": [self.elements,self.name]},
                        {"test_type": self.test_type,
                         "test_key": "view_banned_elements_negative_feedback",
                         "params": [self.elements,self.name]},
                )
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
                         "test_key": "view_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": self.test_type,
                         "test_key": "view_should_exist_negative_feedback",
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
                         "test_key": "view_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": self.test_type,
                         "test_key": "view_should_not_exist_negative_feedback",
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

    def _check_separately_for_all_elements(self, cursor):
        found = []
        for element in self.elements:
            query = f"SELECT * FROM information_schema.views WHERE table_name = '{self.name}' AND view_definition ILIKE '%{element}%'"
            cursor.execute(query)
            result = cursor.fetchall()
            if self.should_exist and len(result) == 0:
                found.append(element)
            elif not self.should_exist and len(result) > 0:
                found.append(element)
        if len(found) == 0: return self.query
        if self.isMaterialized:
            query = f"SELECT * FROM pg_matviews WHERE matviewname = '{self.name}'"
        else:
            query = f"SELECT * FROM pg_views WHERE viewname = '{self.name}'"
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
