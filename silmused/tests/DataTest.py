from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import *
from numbers import Number
import re


class DataTest(TestDefinition):
    test_type = "table_data_test"
    name_parameter = "table_name"

    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, expected_value_query=None, isView=False, column_resolvers=None,
                 custom_feedback=None, llm_check=False, allow_extra_values=False, debug=None, points=0):

        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if expected_value_query is not None and not isinstance(expected_value_query, str):
            raise Exception('Parameter "expected_value_query" must be a string')
        if column_name is not None:
            self.is_count = False if column_name.lower().find("count") == -1 else True
        if column_resolvers is not None and not isinstance(column_resolvers, dict):
            raise Exception('Parameter "column_resolvers" must be a dict')
        if isinstance(expected_value, list):
            self.expected_value_list = True
            if not isinstance(expected_value[0], Number) or len(expected_value) > 2:
                if isinstance(expected_value[0], Number):
                    check_matching_value_types(expected_value, Number)
                else:
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
            self.expected_value_group = None

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
        self.column_resolvers = column_resolvers
        self.allow_extra_values = allow_extra_values
        self.expected_value_query_result = None
        if isView:
            self.test_type = "view_data_test"
            self.name_parameter = "view_name"

    def execute(self, cursor):
        if self.expected_value_query is not None:
            cursor.execute(self.expected_value_query)
            expected_value_query_result = cursor.fetchall()
            expected_values = extract_value_from_tuple(expected_value_query_result)
            self.expected_value = expected_values
            self.expected_value_list = True
            self.expected_value_group = "group"

        if self.column_resolvers is not None:
            self._replace_assessment_objects(cursor)

        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.debug is not None:
            self.debug_output(result)

        if self.expected_value is None:
            return self._assess_result_existence(result)

        if self.expected_value_list:
            if self.expected_value_group == "range":
                return self._assess_range(result)

            if self.expected_value_group == "group":
                return self._assess_value_group(result)

        return self._assess_single_value(result)

    def _assess_result_existence(self, result):
        has_value = any(row[0] is not None for row in result)
        if self.should_exist:
            if self.column_name is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "rows_should_exist_positive_feedback",
                     "params": {self.name_parameter: self.name}},
                    {"test_type": self.test_type,
                     "test_key": "rows_should_exist_negative_feedback",
                     "params": {self.name_parameter: self.name}},
                )
            if self.is_count:
                return super().response(
                    result[0][0] > 0,
                    {"test_type": self.test_type,
                     "test_key": "column_value_should_exist_positive_feedback",
                     "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                    {"test_type": self.test_type,
                     "test_key": "column_value_should_exist_negative_feedback",
                     "params": {self.name_parameter: self.name, "column_name": self.column_name}},

                )
            return super().response(
                has_value,
                {"test_type": self.test_type,
                 "test_key": "column_value_should_exist_positive_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                {"test_type": self.test_type,
                 "test_key": "column_value_should_exist_negative_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name}},

            )
        else:
            if self.column_name is None:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "rows_should_not_exist_positive_feedback",
                     "params": {self.name_parameter: self.name}},
                    {"test_type": self.test_type,
                     "test_key": "rows_should_not_exist_negative_feedback",
                     "params": {self.name_parameter: self.name}},
                )
            return super().response(
                not has_value,
                {"test_type": self.test_type,
                 "test_key": "column_value_should_not_exist_positive_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name}},
                {"test_type": self.test_type,
                 "test_key": "column_value_should_not_exist_negative_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name}},
            )

    def _assess_range(self, result):
        if len(result) == 0:
            return super().response(
                False,
                "",
                {
                    "test_type": self.test_type,
                    "test_key": "test_query_returned_no_rows",
                    "params": {
                        self.name_parameter: self.name,
                        "expected_value": self.expected_value
                    }
                }
            )
        elif len(result) > 1:
            return super().response(
                False,
                "",
                {
                    "test_type": self.test_type,
                    "test_key": "test_query_returned_more_rows_than_expected",
                    "params": {
                        self.name_parameter: self.name,
                        "unexpected_row_count": len(result)
                    }
                }
            )
        actual_value = result[0][0]
        return super().response(
            self.expected_min_value <= actual_value <= self.expected_max_value,
            {"test_type": self.test_type,
             "test_key": "expected_value_range_positive_feedback",
             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                        "expected_min_value": self.expected_min_value,
                        "expected_max_value": self.expected_max_value,
                        "actual_value": actual_value}},
            {"test_type": self.test_type,
             "test_key": "expected_value_range_negative_feedback",
             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                        "expected_min_value": self.expected_min_value,
                        "expected_max_value": self.expected_max_value,
                        "actual_value": actual_value}})

    def _assess_value_group(self, result):
        expected_values = [
            normalize_expected_value(value)
            for value in self.expected_value
        ]
        assessment_result = check_all_results(result, expected_values, self.allow_extra_values)

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
        return super().response(
            assessment_result['assessment'],
            {"test_type": self.test_type,
             "test_key": "expected_values_group_positive_feedback",
             "params": {self.name_parameter: self.name, "column_name": self.column_name}},
            {},
        )

    def _assess_single_value(self, result):
        if len(result) == 0:
            if not self.should_exist:
                return super().response(
                    True,
                    {"test_type": self.test_type,
                     "test_key": "expected_value_should_not_exist_positive_feedback",
                     "params": {self.name_parameter: self.name, "column_name": self.column_name,
                                "expected_value": self.expected_value, "actual_value": ""}},
                    {}
                )
            return super().response(
                False,
                "",
                {"test_type": self.test_type, "test_key": "test_query_returned_no_rows",
                 "params": {self.name_parameter: self.name, "expected_value": self.expected_value}}
            )
        elif len(result) > 1:
            return super().response(
                False,
                "",
                {"test_type": self.test_type,
                 "test_key": "test_query_returned_more_rows_than_expected",
                 "params": {self.name_parameter: self.name, "unexpected_row_count": len(result)}}
            )

        actual_value = result[0][0]
        expected_value = normalize_expected_value(self.expected_value)

        assessment = actual_value == expected_value

        if self.should_exist:
            return super().response(
                assessment,
                {"test_type": self.test_type,
                 "test_key": "expected_value_should_exist_positive_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name,
                            "expected_value": self.expected_value}},
                {"test_type": self.test_type,
                 "test_key": "expected_value_should_exist_negative_feedback",
                 "params": {self.name_parameter: self.name, "column_name": self.column_name,
                            "expected_value": self.expected_value, "actual_value": actual_value}},
            )
        return super().response(
            not assessment,
            {"test_type": self.test_type,
             "test_key": "expected_value_should_not_exist_positive_feedback",
             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                        "expected_value": self.expected_value, "actual_value": actual_value}},
            {"test_type": self.test_type,
             "test_key": "expected_value_should_not_exist_negative_feedback",
             "params": {self.name_parameter: self.name, "column_name": self.column_name,
                        "expected_value": self.expected_value, "actual_value": actual_value}},
        )

    def _replace_assessment_objects(self, cursor):
        cursor.execute(
            f"SELECT column_name, ordinal_position "
            f"FROM information_schema.columns "
            f"WHERE table_schema = 'public' "
            f"AND table_name = '{self.name}' "
            f"ORDER BY ordinal_position"
        )
        available_columns = dict(cursor.fetchall())

        columns_to_resolve = set()

        if self.column_name is not None:
            columns_to_resolve.add(self.column_name)

        if self.where is not None:
            placeholders = re.findall(
                r"\$([A-Za-z_][A-Za-z0-9_]*)",
                self.where
            )

            columns_to_resolve.update(placeholders)

        resolved_columns = {}

        for column_name in columns_to_resolve:
            resolved_name = self.resolve_object_name(column_name, available_columns, self.column_resolvers)

            if resolved_name is not None:
                resolved_columns[column_name] = resolved_name

        self.column_name = resolved_columns.get(self.column_name, self.column_name)
        resolved_where = self.where

        if resolved_where is not None:
            for original_name, resolved_name in resolved_columns.items():
                resolved_where = resolved_where.replace(f"${original_name}", resolved_name)
        self.where = resolved_where
        self.query = self.query_builder(
            f"SELECT {self.column_name if self.column_name is not None else '*'} FROM {self.name}")

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
            if self.expected_value_query is not None: print(
                f"expected_value_query_result: {self.expected_value_query_result}")
            if self.isView is not None: print(f"isView: {self.isView}")
            if self.column_name_fallback is not None: print(f"column_name_fallback: {self.column_name_fallback}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
            if self.elements is not None: print(f"elements: {self.elements}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.points is not None: print(f"points: {self.points}")
            if isinstance(self.expected_value, list):
                if self.expected_value_list is not None: print(f"expected_value_list: {self.expected_value_list}")
                if self.allow_extra_values is not None: print(f"allow_extra_values: {self.allow_extra_values}")
                if not isinstance(self.expected_value[0], str):
                    if self.expected_value_group is not None: print(
                        f"expected_value_group: {self.expected_value_group}")
                    if self.expected_min_value is not None: print(f"expected_min_value: {self.expected_min_value}")
                    if self.expected_max_value is not None: print(f"expected_max_value: {self.expected_max_value}")
        if self.debug not in ['DEBUG', 'ALL']:
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")
