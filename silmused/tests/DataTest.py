from silmused.tests.TestDefinition import TestDefinition


# TODO split this into TableDataTest and ViewDataTest, so that feedback would be more
# TODO expected_value - add option to check the value between a set of data ex. 105-108
class DataTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, isView=False, points=0):

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
        self.isView=isView

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()
        if not self.isView:
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
                            # TODO Should check if all results are not None, line 148 also
                            return super().response(
                                len(result) > 0 and result[0][0] is not None,
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
                         "test_key": "table_expected_value_should_exist_positive_feedback",
                         "params": [self.expected_value, self.name, self.column_name]},
                        {"test_type": "data_test",
                         "test_key": "table_expected_value_should_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    )
                else:
                    return super().response(
                        str(result[0][0]) != str(self.expected_value),
                        {"test_type": "data_test",
                         "test_key": "table_expected_value_should_not_exist_positive_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                        {"test_type": "data_test",
                         "test_key": "table_expected_value_should_not_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    )
        # isView = True
        else:
            if self.expected_value is None:
                if self.should_exist:
                    if self.column_name is None:
                        return super().response(
                            len(result) > 0,
                            {"test_type": "data_test",
                             "test_key": "view_not_expected_value_should_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": "data_test",
                             "test_key": "view_not_expected_value_should_exist_negative_feedback",
                             "params": [self.name]},

                        )
                    else:
                        if self.is_count:
                            return super().response(
                                result[0][0] > 0,
                                {"test_type": "data_test",
                                 "test_key": "view_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": "data_test",
                                 "test_key": "view_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )
                        else:
                            return super().response(
                                len(result) > 0 and result[0][0] is not None,
                                {"test_type": "data_test",
                                 "test_key": "view_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": "data_test",
                                 "test_key": "view_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )

                else:
                    if self.column_name is None:
                        return super().response(
                            len(result) == 0,
                            {"test_type": "data_test",
                             "test_key": "view_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": "data_test",
                             "test_key": "view_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name]},

                        )
                    else:
                        return super().response(
                            len(result) == 0,
                            {"test_type": "data_test",
                             "test_key": "view_column_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name, self.column_name]},
                            {"test_type": "data_test",
                             "test_key": "view_column_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name, self.column_name]},

                        )
            # expected value is not None
            else:
                if self.should_exist:
                    # TODO add type check

                    return super().response(
                        str(result[0][0]) == str(self.expected_value),
                        {"test_type": "data_test",
                         "test_key": "view_expected_value_should_exist_positive_feedback",
                         "params": [self.expected_value, self.name, self.column_name]},
                        {"test_type": "data_test",
                         "test_key": "view_expected_value_should_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    )
                else:
                    return super().response(
                        str(result[0][0]) != str(self.expected_value),
                        {"test_type": "data_test",
                         "test_key": "view_expected_value_should_not_exist_positive_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                        {"test_type": "data_test",
                         "test_key": "view_expected_value_should_not_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    )

