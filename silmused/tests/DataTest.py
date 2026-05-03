from silmused.tests.TestDefinition import TestDefinition


# TODO split this into TableDataTest and ViewDataTest, so that feedback code would be more readable
# But this will just duplicate code...
class DataTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, expected_value_query=None, isView=False, column_name_fallback=None,
                 custom_feedback=None, llm_check=False, debug=None, points=0):

        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if expected_value_query is not None and not isinstance(expected_value_query, str):
            raise Exception('Parameter "expected_value_query" must be a string')
        if column_name is not None:
            self.is_count = False if column_name.lower().find("count") == -1 else True
        if column_name_fallback is not None and not isinstance(column_name_fallback, list):
            raise Exception('Parameter "column_name_fallback" must be a list')
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
            custom_feedback=custom_feedback,
            expected_value_query=expected_value_query,
            llm_check=llm_check,
            debug=debug,
        )

        self.column_name = column_name
        self.where = where
        self.join = join
        self.isView = isView
        self.column_name_fallback = column_name_fallback
        self.test_type = "data_test"

    def execute(self, cursor):
        if self.expected_value_query is not None:
            cursor.execute(self.expected_value_query)
            result = cursor.fetchall()
            self.expected_value = result[0][0]
        if self.column_name_fallback is not None:
            self.column_name = self.check_alternative_columns(cursor)
            self.query = (f"SELECT {self.column_name if self.column_name is not None else '*'} FROM {self.name}" +
                          f" WHERE ({self.where})") if self.where is not None else ""
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.debug is not None: self.debug_output(result)

        # Result assessment
        if not self.isView:
            if self.expected_value is None:
                if self.should_exist:
                    if self.column_name is None:
                        return super().response(
                            len(result) > 0,
                            {"test_type": self.test_type,
                             "test_key": "table_not_expected_value_should_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": self.test_type,
                             "test_key": "table_not_expected_value_should_exist_negative_feedback",
                             "params": [self.name]},
                        )
                    else:
                        if self.is_count:
                            return super().response(
                                result[0][0] > 0,
                                {"test_type": self.test_type,
                                 "test_key": "table_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "table_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )
                        else:
                            # TODO Should check if all results are not None
                            return super().response(
                                len(result) > 0 and result[0][0] is not None,
                                {"test_type": self.test_type,
                                 "test_key": "table_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "table_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )

                else:
                    if self.column_name is None:
                        return super().response(
                            len(result) == 0,
                            {"test_type": self.test_type,
                             "test_key": "table_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": self.test_type,
                             "test_key": "table_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name]},
                        )
                    else:
                        return super().response(
                            len(result) == 0,
                            {"test_type": self.test_type,
                             "test_key": "table_column_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name, self.column_name]},
                            {"test_type": self.test_type,
                             "test_key": "table_column_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name, self.column_name]},

                        )
            # expected value is not None
            else:
                if self.should_exist:
                    if len(result) == 0:
                        return super().response(
                            False,
                            "",
                            {"test_type": self.test_type,
                             "test_key": "view_query_no_result",
                             "params": [self.expected_value, self.name]},
                        )
                    if self.expected_value == 'NULL' or self.expected_value == 'None':
                        if result[0][0] is None and len(result) > 0:
                            return super().response(
                                result[0][0] is None,
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_negative_feedback",
                                 "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                            )
                        else:
                            return super().response(
                                False,
                                '',
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_no_result_negative_feedback",
                                 "params": [self.name, self.column_name]},
                            )
                    elif self.expected_value_list:
                        if self.expected_value_group == "numbers":
                            if len(result) > 0:
                                return super().response(
                                    self.expected_min_value <= result[0][0] <= self.expected_max_value,
                                    {"test_type": self.test_type,
                                     "test_key": "table_expected_value_group_numbers_positive_feedback",
                                     "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                                self.name, self.column_name]},
                                    {"test_type": self.test_type,
                                     "test_key": "table_expected_value_group_numbers_negative_feedback",
                                     "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                                self.name, self.column_name]},
                                )
                            else:
                                return super().response(
                                    False,
                                    '',
                                        {"test_type": self.test_type,
                                     "test_key": "table_expected_value_group_numbers_no_result_negative_feedback",
                                     "params": [self.name, self.column_name]},
                                )
                        elif self.expected_value_group == "strings":
                            if len(result) > 0:
                                return super().response(
                                    result[0][0] in self.expected_value,
                                    {"test_type": self.test_type,
                                     "test_key": "table_expected_value_group_strings_positive_feedback",
                                     "params": [str(result[0][0]), self.expected_value, self.column_name]},
                                    {"test_type": self.test_type,
                                     "test_key": "table_expected_value_group_strings_negative_feedback",
                                     "params": [str(result[0][0]), self.expected_value, self.column_name]},
                                )
                            else:
                                return super().response(
                                    False,
                                    '',
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_numbers_no_result_negative_feedback",
                                     "params": [self.name, self.column_name]},
                                )
                    else:
                        if not isinstance(result[0][0], str) and not isinstance(self.expected_value, str):
                            return super().response(
                                result[0][0] == self.expected_value,
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_negative_feedback",
                                 "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                            )
                        else:
                            return super().response(
                                str(result[0][0]) == str(self.expected_value),
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "table_expected_value_should_exist_negative_feedback",
                                 "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                            )
                else:
                    return super().response(
                        str(result[0][0]) != str(self.expected_value),
                        {"test_type": self.test_type,
                         "test_key": "table_expected_value_should_not_exist_positive_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                        {"test_type": self.test_type,
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
                            {"test_type": self.test_type,
                             "test_key": "view_not_expected_value_should_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": self.test_type,
                             "test_key": "view_not_expected_value_should_exist_negative_feedback",
                             "params": [self.name]},

                        )
                    else:
                        if self.is_count:
                            return super().response(
                                result[0][0] > 0,
                                {"test_type": self.test_type,
                                 "test_key": "view_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "view_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )
                        else:
                            # TODO Should check if all results are not None
                            return super().response(
                                len(result) > 0 and result[0][0] is not None,
                                {"test_type": self.test_type,
                                 "test_key": "view_column_not_expected_value_should_exist_positive_feedback",
                                 "params": [self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "view_column_not_expected_value_should_exist_negative_feedback",
                                 "params": [self.name, self.column_name]},

                            )
                else:
                    if self.column_name is None:
                        return super().response(
                            len(result) == 0,
                            {"test_type": self.test_type,
                             "test_key": "view_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name]},
                            {"test_type": self.test_type,
                             "test_key": "view_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name]},
                        )
                    else:
                        return super().response(
                            len(result) == 0,
                            {"test_type": self.test_type,
                             "test_key": "view_column_not_expected_value_should_not_exist_positive_feedback",
                             "params": [self.name, self.column_name]},
                            {"test_type": self.test_type,
                             "test_key": "view_column_not_expected_value_should_not_exist_negative_feedback",
                             "params": [self.name, self.column_name]},
                        )
            # expected value is not None
            else:
                if self.should_exist:
                    if len(result) == 0:
                        return super().response(
                            False,
                            "",
                            {"test_type": self.test_type,
                             "test_key": "table_query_no_result",
                             "params": [self.expected_value, self.name]},
                        )
                    if self.expected_value == 'NULL' or self.expected_value == 'None':
                        if result[0][0] is None and len(result) > 0:
                            return super().response(
                                result[0][0] is None,
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.name, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_negative_feedback",
                                 "params": ['NULL', str(result[0][0]), self.name, self.column_name]},
                            )
                        else:
                            return super().response(
                                False,
                                '',
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_no_result_negative_feedback",
                                 "params": [self.name, self.column_name]},
                            )
                    elif self.expected_value_list:
                        if self.expected_value_group == "numbers":
                            if len(result) > 0:
                                return super().response(
                                    self.expected_min_value <= result[0][0] <= self.expected_max_value,
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_numbers_positive_feedback",
                                     "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                                self.name, self.column_name]},
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_numbers_negative_feedback",
                                     "params": [str(result[0][0]), self.expected_min_value, self.expected_max_value,
                                                self.name, self.column_name]},
                                )
                            else:
                                return super().response(
                                    False,
                                    '',
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_numbers_no_result_negative_feedback",
                                     "params": [self.name, self.column_name]},
                                )
                        elif self.expected_value_group == "strings":
                            if len(result) > 0:
                                return super().response(
                                    result[0][0] in self.expected_value,
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_strings_positive_feedback",
                                     "params": [str(result[0][0]), self.expected_value, self.column_name]},
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_strings_negative_feedback",
                                     "params": [str(result[0][0]), self.expected_value, self.column_name]},
                                )
                            else:
                                return super().response(
                                    False,
                                    '',
                                    {"test_type": self.test_type,
                                     "test_key": "view_expected_value_group_numbers_no_result_negative_feedback",
                                     "params": [self.name, self.column_name]},
                                )
                    else:
                        if not isinstance(result[0][0], str) and not isinstance(self.expected_value, str):
                            return super().response(
                                result[0][0] == self.expected_value,
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_negative_feedback",
                                 "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                            )
                        else:
                            return super().response(
                                str(result[0][0]) == str(self.expected_value),
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_positive_feedback",
                                 "params": [self.expected_value, self.column_name]},
                                {"test_type": self.test_type,
                                 "test_key": "view_expected_value_should_exist_negative_feedback",
                                 "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                            )
                else:
                    return super().response(
                        str(result[0][0]) != str(self.expected_value),
                        {"test_type": self.test_type,
                         "test_key": "view_expected_value_should_not_exist_positive_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                        {"test_type": self.test_type,
                         "test_key": "view_expected_value_should_not_exist_negative_feedback",
                         "params": [self.expected_value, str(result[0][0]), self.name, self.column_name]},
                    )
        return super().response(
            str(result[0][0]) != str(self.expected_value),
            {"test_type": self.test_type,
             "test_key": "no_feedback",
             "params": []},
            {"test_type": self.test_type,
             "test_key": "no_feedback",
             "params": []},
        )

    def check_alternative_columns(self, cursor):
        for c_name in self.column_name_fallback:
            query = (f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.name}' "
                     f"AND column_name ILIKE '{c_name}'")
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result[0][0]) > 0:
                return result[0][0]
        return self.column_name

    def debug_output(self, result):
        print('DATA TEST DEBUG: ')
        if self.debug == 'DEBUG':
            if self.title is not None: print(f"Test title: {self.title}")
            print(f"query: {self.query}")
            print(f"result: {result}")
        if self.debug == 'ALL':
            if self.name is not None: print(f"name: {self.name}")
            if self.arguments is not None: print(f"arguments: {self.arguments}")
            if self.column_name is not None: print(f"column_name: {self.column_name}")
            if self.where is not None: print(f"where: {self.where}")
            if self.join is not None: print(f"join: {self.join}")
            if self.description is not None: print(f"description: {self.description}")
            if self.expected_value is not None: print(f"expected_value: {self.expected_value}")
            if self.expected_count is not None: print(f"expected_count: {self.expected_count}")
            if self.expected_value_query is not None: print(f"expected_value_query: {self.expected_value_query}")
            if self.isView is not None: print(f"isView: {self.isView}")
            if self.column_name_fallback is not None: print(f"column_name_fallback: {self.column_name_fallback}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
            if self.elements is not None: print(f"elements: {self.elements}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.points is not None: print(f"points: {self.points}")
            if self.expected_value_list is not None: print(f"expected_value_list: {self.expected_value_list}")
            if self.expected_value_group is not None: print(f"expected_value_group: {self.expected_value_group}")
            if self.expected_min_value is not None: print(f"expected_min_value: {self.expected_min_value}")
            if self.expected_max_value is not None: print(f"expected_max_value: {self.expected_max_value}")
            if self.test_type is not None: print(f"test_type: {self.test_type}")
        if self.debug != 'DEBUG' or self.debug != 'ALL':
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")
