from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import *
from numbers import Number


class DataTest(TestDefinition):
    test_type = "table_data_test"
    name_parameter = "table_name"

    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, expected_value_query=None, isView=False, column_name_fallback=None,
                 custom_feedback=None, llm_check=False, allow_extra_values=False, debug=None, points=0):

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
            if not isinstance(expected_value[0], Number) or len(expected_value) > 2:
                check_matching_value_types(expected_value, type(expected_value[0]))
                self.expected_value_group = "group"
            else:
                check_matching_value_types(expected_value, Number)
                self.expected_value_group = "range"
                min_value = None
                max_value = None
                for value in expected_value:
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
        self.allow_extra_values = allow_extra_values
        if isView:
            self.test_type = "view_data_test"
            self.name_parameter = "view_name"

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
        if self.expected_value is None:
            if self.should_exist:
                if self.column_name is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": self.test_type,
                         "test_key": "not_expected_value_should_exist_positive_feedback",
                         "params": {self.name_parameter: self.name}},
                        {"test_type": self.test_type,
                         "test_key": "not_expected_value_should_exist_negative_feedback",
                         "params": {self.name_parameter: self.name}},
                    )
                else:
                    if self.is_count:
                        return super().response(
                            result[0][0] > 0,
                            {"test_type": self.test_type,
                             "test_key": "column_not_expected_value_should_exist_positive_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                            {"test_type": self.test_type,
                             "test_key": "column_not_expected_value_should_exist_negative_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name}},

                        )
                    else:
                        return super().response(
                            len(result) > 0 and result[0][0] is not None,
                            {"test_type": self.test_type,
                             "test_key": "column_not_expected_value_should_exist_positive_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                            {"test_type": self.test_type,
                             "test_key": "column_not_expected_value_should_exist_negative_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name}},

                        )

            else:
                if self.column_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "not_expected_value_should_not_exist_positive_feedback",
                         "params": {self.name_parameter: self.name}},
                        {"test_type": self.test_type,
                         "test_key": "not_expected_value_should_not_exist_negative_feedback",
                         "params": {self.name_parameter: self.name}},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": self.test_type,
                         "test_key": "column_not_expected_value_should_not_exist_positive_feedback",
                         "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                        {"test_type": self.test_type,
                         "test_key": "column_not_expected_value_should_not_exist_negative_feedback",
                         "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                    )
        # expected value is not None
        else:
            if self.should_exist:
                if len(result) == 0:
                    return super().response(
                        False,
                        "",
                        {"test_type": self.test_type,
                         "test_key": "test_query_returned_no_rows",
                         "params": {self.name_parameter: self.name, "expected_value": self.expected_value}},
                    )
                if self.expected_value == 'NULL' or self.expected_value == 'None':
                    return super().response(
                        result[0][0] is None,
                        {"test_type": self.test_type,
                         "test_key": "expected_value_should_exist_positive_feedback",
                         "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                    "expected_value": self.expected_value}},
                        {"test_type": self.test_type,
                         "test_key": "expected_value_should_exist_negative_feedback",
                         "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                    "expected_value": self.expected_value, "actual_value": str(result[0][0])}},
                    )
                elif self.expected_value_list:
                    if self.expected_value_group == "range":
                        return super().response(
                            self.expected_min_value <= result[0][0] <= self.expected_max_value,
                            {"test_type": self.test_type,
                             "test_key": "expected_value_range_positive_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_min_value": self.expected_min_value,
                                        "expected_max_value": self.expected_max_value,
                                        "actual_value": result[0][0]}},
                            {"test_type": self.test_type,
                             "test_key": "expected_value_range_negative_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_min_value": self.expected_min_value,
                                        "expected_max_value": self.expected_max_value,
                                        "actual_value": result[0][0]}},
                        )
                    elif self.expected_value_group == "group":
                        assessment_result = check_all_results(result, self.expected_value, self.allow_extra_values)
                        if len(assessment_result["unexpected_value"]) > 0 and len(assessment_result["expected_value"]) > 0:
                            return super().response(
                                assessment_result['assessment'],
                                {},
                                {"test_type": self.test_type,
                                 "test_key": "expected_values_group_missing_and_unexpected_negative_feedback",
                                 "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                            "expected_values": assessment_result["expected_value"],
                                            "unexpected_values": assessment_result["unexpected_value"]}},
                            )
                        elif len(assessment_result["unexpected_value"]) > 0:
                            return super().response(
                                assessment_result['assessment'],
                                {},
                                {"test_type": self.test_type,
                                 "test_key": "expected_values_group_unexpected_negative_feedback",
                                 "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                            "unexpected_values": assessment_result["unexpected_value"]}},
                            )
                        elif len(assessment_result["expected_value"]) > 0:
                            return super().response(
                                assessment_result['assessment'],
                                {},
                                {"test_type": self.test_type,
                                 "test_key": "expected_values_group_missing_negative_feedback",
                                 "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                            "expected_values": assessment_result["expected_value"]}},
                            )
                        else:
                            return super().response(
                                assessment_result['assessment'],
                                {"test_type": self.test_type,
                                 "test_key": "expected_values_group_positive_feedback",
                                 "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                                {},
                            )
                else:
                    if not isinstance(result[0][0], str) and not isinstance(self.expected_value, str):
                        return super().response(
                            result[0][0] == self.expected_value,
                            {"test_type": self.test_type,
                             "test_key": "expected_value_should_exist_positive_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_value": self.expected_value}},
                            {"test_type": self.test_type,
                             "test_key": "expected_value_should_exist_negative_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_value": self.expected_value, "actual_value": str(result[0][0])}},
                        )
                    else:
                        return super().response(
                            str(result[0][0]) == str(self.expected_value),
                            {"test_type": self.test_type,
                             "test_key": "expected_value_should_exist_positive_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_value": self.expected_value}},
                            {"test_type": self.test_type,
                             "test_key": "expected_value_should_exist_negative_feedback",
                             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                        "expected_value": self.expected_value, "actual_value": str(result[0][0])}},
                        )
            else:
                return super().response(
                    str(result[0][0]) != str(self.expected_value),
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_not_exist_positive_feedback",
                     "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                "expected_value": self.expected_value, "actual_value": str(result[0][0])}},
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_not_exist_negative_feedback",
                     "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                "expected_value": self.expected_value, "actual_value": str(result[0][0])}},
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
            if self.test_type is not None: print(f"test_type: {self.test_type}")
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
            if isinstance(self.expected_value, list):
                if self.expected_value_list is not None: print(f"expected_value_list: {self.expected_value_list}")
                if not isinstance(self.expected_value[0], str):
                    if self.expected_value_group is not None: print(
                        f"expected_value_group: {self.expected_value_group}")
                    if self.expected_min_value is not None: print(f"expected_min_value: {self.expected_min_value}")
                    if self.expected_max_value is not None: print(f"expected_max_value: {self.expected_max_value}")
        if self.debug not in ['DEBUG', 'ALL']:
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")
