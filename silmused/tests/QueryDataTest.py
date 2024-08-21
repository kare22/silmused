from silmused.tests.TestDefinition import TestDefinition


class QueryDataTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, points=0):

        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if column_name is not None:
            self.is_count = False if column_name.lower().find("count") == -1 else True
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
        else:
            self.expected_value_list = False

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
                        {"test_type": "query_data_test",
                         "test_key": "query_not_expected_value_should_exist_positive_feedback"},
                        {"test_type": "query_data_test",
                         "test_key": "query_not_expected_value_should_exist_negative_feedback"},

                    )
                else:
                    if self.is_count:
                        return super().response(
                            result[0][0] > 0,
                            {"test_type": "query_data_test",
                             "test_key": "query_column_not_expected_value_should_exist_positive_feedback",
                             "params": [self.column_name]},
                            {"test_type": "query_data_test",
                             "test_key": "query_column_not_expected_value_should_exist_negative_feedback",
                             "params": [self.column_name]},

                        )
                    # Same feedback test_keys
                    else:
                        # TODO Should check if all results are not None, line 148 also
                        return super().response(
                            len(result) > 0 and result[0][0] is not None,
                            {"test_type": "query_data_test",
                             "test_key": "query_column_not_expected_value_should_exist_positive_feedback",
                             "params": [self.column_name]},
                            {"test_type": "query_data_test",
                             "test_key": "query_column_not_expected_value_should_exist_negative_feedback",
                             "params": [self.column_name]},
                        )
            # should_exist = False
            else:
                if self.column_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_data_test",
                         "test_key": "query_not_expected_value_should_not_exist_positive_feedback"},
                        {"test_type": "query_data_test",
                         "test_key": "query_not_expected_value_should_not_exist_negative_feedback"},

                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "query_data_test",
                         "test_key": "query_column_not_expected_value_should_not_exist_positive_feedback",
                         "params": [self.column_name]},
                        {"test_type": "query_data_test",
                         "test_key": "query_column_not_expected_value_should_not_exist_negative_feedback",
                         "params": [self.column_name]},

                    )
        # expected value is not None
        else:
            if self.should_exist:
                if self.expected_value == 'NULL' or self.expected_value == 'None':
                    if result[0][0] is None and len(result) > 0:
                        return super().response(
                            result[0][0] is None,
                            {"test_type": "query_data_test",
                             "test_key": "query_expected_value_should_exist_positive_feedback",
                             "params": [self.expected_value, self.name, self.column_name]},
                            {"test_type": "query_data_test",
                             "test_key": "query_expected_value_should_exist_negative_feedback",
                             "params": ['NULL', str(result[0][0]), self.name, self.column_name]},
                        )
                elif self.expected_value_list:
                    if self.expected_value_group == "numbers":
                        if len(result) > 0:
                            return super().response(
                                self.expected_min_value <= result[0][0] <= self.expected_max_value,
                                {"test_type": "query_data_test",
                                 "test_key": "query_expected_value_group_numbers_positive_feedback",
                                 "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                            self.column_name]},
                                {"test_type": "query_data_test",
                                 "test_key": "query_expected_value_group_numbers_negative_feedback",
                                 "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                            self.column_name]},
                            )
                    elif self.expected_value_group == "strings":
                        if len(result) > 0:
                            return super().response(
                                result[0][0] in self.expected_value,
                                {"test_type": "query_data_test",
                                 "test_key": "query_expected_value_group_strings_positive_feedback",
                                 "params": [str(result[0][0]), self.expected_value, self.column_name]},
                                {"test_type": "query_data_test",
                                 "test_key": "query_expected_value_group_strings_negative_feedback",
                                 "params": [str(result[0][0]), self.expected_value, self.column_name]},
                            )
                else:
                    # TODO No result found should have a feedback
                    # TODO add type check
                    return super().response(
                        str(result[0][0]) == str(self.expected_value),
                        {"test_type": "query_data_test",
                         "test_key": "query_expected_value_should_exist_positive_feedback",
                         "params": [self.expected_value, self.column_name]},
                        {"test_type": "query_data_test",
                         "test_key": "query_expected_value_should_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.column_name]},
                    )
            else:
                return super().response(
                    str(result[0][0]) != str(self.expected_value),
                    {"test_type": "query_data_test",
                     "test_key": "query_expected_value_should_not_exist_positive_feedback",
                     "params": [self.expected_value, str(result[0][0]), self.column_name]},
                    {"test_type": "query_data_test",
                     "test_key": "query_expected_value_should_not_exist_negative_feedback",
                     "params": [self.expected_value, str(result[0][0]), self.column_name]},
                )
