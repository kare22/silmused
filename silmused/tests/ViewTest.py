from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class ViewTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, expected_value=None, should_exist=True,
                 where=None, description=None, custom_feedback=None, isMaterialized=False, elements=None, points=0):
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
                raise AttributeError('Parameter banned_arguments must be list or string')

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
        )

        self.column_name = column_name
        self.where = where
        self.isMaterialized = isMaterialized

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.isMaterialized:
            if self.elements is not None:
                if self.should_exist:
                    if self.custom_feedback is None:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "view_test",
                             "test_key": "mat_view_required_elements_positive_feedback",
                             "params": [self.elements,self.name]},
                            {"test_type": "query_structure_test",
                             "test_key": "mat_view_required_elements_negative_feedback",
                             "params": [self.elements,self.name]},
                        )
                    else:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "view_test",
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
                            {"test_type": "view_test",
                             "test_key": "mat_view_banned_elements_positive_feedback",
                             "params": [self.elements,self.name]},
                            {"test_type": "query_structure_test",
                             "test_key": "mat_view_banned_elements_negative_feedback",
                             "params": [self.elements,self.name]},
                        )
                    else:
                        return super().response(
                            len(result) == 0,
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "query_structure_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
            elif self.should_exist:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "view_test",
                         "test_key": "mat_view_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "view_test",
                         "test_key": "mat_view_should_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        False,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "view_test",
                         "test_key": "mat_view_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "view_test",
                         "test_key": "mat_view_should_not_exist_negative_feedback",
                         "params": [self.name]},
                    )
                else:
                    return super().response(
                        False,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
        if self.elements is not None:
            if self.should_exist:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) > 0,
                            {"test_type": "view_test",
                             "test_key": "view_required_elements_positive_feedback",
                             "params": [self.elements,self.name]},
                            {"test_type": "query_structure_test",
                             "test_key": "view_required_elements_negative_feedback",
                             "params": [self.elements,self.name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.custom_feedback is None:
                    return super().response(
                        len(result) == 0,
                            {"test_type": "view_test",
                             "test_key": "view_banned_elements_positive_feedback",
                             "params": [self.elements,self.name]},
                            {"test_type": "query_structure_test",
                             "test_key": "view_banned_elements_negative_feedback",
                             "params": [self.elements,self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
        if self.expected_value is not None:
            # TODO Is this needed?
            # What is this test checking? result 0,0 is database name, maybe this should check if the value is found in result?
            if self.should_exist:
                if self.custom_feedback is None:
                # print(self.title, result[0][0])
                    return super().response(
                        len(result) != 0 and result[0][0] == self.expected_value,
                        {"test_type": "view_test",
                         "test_key": "expected_value_should_exist_positive_feedback",
                         "params": [self.query]},
                        {"test_type": "view_test",
                         "test_key": "expected_value_should_exist_negative_feedback",
                         "params": [self.query, self.expected_value]},
                    )
                else:
                    return super().response(
                        False,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
            else:
                if self.custom_feedback is None:
                # print(self.title, result[0][0])
                    return super().response(
                        len(result) == 0 or result[0][0] != self.expected_value,
                        {"test_type": "view_test",
                         "test_key": "expected_value_should_not_exist_positive_feedback",
                         "params": [self.query]},
                        {"test_type": "view_test",
                         "test_key": "expected_value_should_not_exist_negative_feedback",
                         "params": [self.query, self.expected_value]},
                    )
                else:
                    return super().response(
                        False,
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                        {"test_type": "view_test",
                         "test_key": "custom_feedback",
                         "params": [self.custom_feedback]},
                    )
        else:
            if self.should_exist:
                if self.column_name is None:
                    if self.custom_feedback is None:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "view_test",
                             "test_key": "view_should_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": "view_test",
                             "test_key": "view_should_exist_negative_feedback",
                             "params": [self.name]},
                        )
                    else:
                        return super().response(
                            False,
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
                else:
                    if self.custom_feedback is None:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "view_test",
                             "test_key": "column_should_exist_positive_feedback",
                             "params": [self.column_name, self.name]},
                            {"test_type": "view_test",
                             "test_key": "column_should_exist_negative_feedback",
                             "params": [self.column_name, self.name]},
                        )
                    else:
                        return super().response(
                            False,
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
            else:
                if self.column_name is None:
                    if self.custom_feedback is None:
                        return super().response(
                            len(result) == 0,
                            {"test_type": "view_test",
                             "test_key": "view_should_not_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": "view_test",
                             "test_key": "view_should_not_exist_negative_feedback",
                             "params": [self.name]},
                        )
                    else:
                        return super().response(
                            False,
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )
                else:
                    if self.custom_feedback is None:
                        return super().response(
                            len(result) == 0,
                            {"test_type": "view_test",
                             "test_key": "column_should_not_exist_positive_feedback",
                             "params": [self.column_name, self.name]},
                            {"test_type": "view_test",
                             "test_key": "column_should_not_exist_negative_feedback",
                             "params": [self.column_name, self.name]},
                        )
                    else:
                        return super().response(
                            False,
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                            {"test_type": "view_test",
                             "test_key": "custom_feedback",
                             "params": [self.custom_feedback]},
                        )