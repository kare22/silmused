from silmused.tests.TestDefinition import TestDefinition


# TODO raname to TableDataTest ??
class DataTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, points=0):

        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if column_name is not None:
            self.is_count = False if column_name.lower().find("count") == -1 else True
        super().__init__(
            name=name,
            title=title,
            where=where,
            join=join,
            points=points,
            description=description,
            query=f"SELECT {column_name if column_name is not None else '*'} FROM {name}",
            should_exist=should_exist,
            expected_value=expected_value,
        )

        self.column_name = column_name
        self.where = where
        self.join = join

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.expected_value is None:
            if self.should_exist:
                if self.column_name is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "data_test",
                         "test_key": "table_not_expected_value_should_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "data_test",
                         "test_key": "table_not_expected_value_should_exist_negative_feedback",
                         "params": [self.name]},

                    )
                else:
                    if self.is_count:
                        return super().response(
                            result[0][0] > 0,
                            {"test_type": "data_test",
                             "test_key": "table_column_not_expected_value_should_exist_positive_feedback",
                             "params": [self.name, self.column_name]},
                            {"test_type": "data_test",
                             "test_key": "table_column_not_expected_value_should_exist_negative_feedback",
                             "params": [self.name, self.column_name]},

                        )
                    else:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "data_test",
                             "test_key": "table_column_not_expected_value_should_exist_positive_feedback",
                             "params": [self.name, self.column_name]},
                            {"test_type": "data_test",
                             "test_key": "table_column_not_expected_value_should_exist_negative_feedback",
                             "params": [self.name, self.column_name]},

                        )

            else:
                if self.column_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "data_test",
                         "test_key": "table_not_expected_value_should_not_exist_positive_feedback",
                         "params": [self.name]},
                        {"test_type": "data_test",
                         "test_key": "table_not_expected_value_should_not_exist_negative_feedback",
                         "params": [self.name]},

                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "data_test",
                         "test_key": "table_column_not_expected_value_should_not_exist_positive_feedback",
                         "params": [self.name, self.column_name]},
                        {"test_type": "data_test",
                         "test_key": "table_column_not_expected_value_should_not_exist_negative_feedback",
                         "params": [self.name, self.column_name]},

                    )
        # expected value is not None
        else:
            if self.should_exist:
                # TODO add type check

                return super().response(
                    str(result[0][0]) == str(self.expected_value),
                    {"test_type": "data_test",
                     "test_key": "expected_value_should_exist_positive_feedback",
                     "params": [self.expected_value, self.name, self.column_name]},
                    {"test_type": "data_test",
                     "test_key": "expected_value_should_exist_negative_feedback",
                     "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                )
            else:
                return super().response(
                    str(result[0][0]) != str(self.expected_value),
                    {"test_type": "data_test",
                     "test_key": "expected_value_should_not_exist_positive_feedback",
                     "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    {"test_type": "data_test",
                     "test_key": "expected_value_should_not_exist_negative_feedback",
                     "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                )
