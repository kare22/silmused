"""
Tests for DataTest feedback messages.
Tests all feedback keys from the data_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.DataTest import DataTest
from silmused.tests.ViewDataTest import ViewDataTest
from silmused.Translator import Translator


@pytest.fixture(params=[DataTest, ViewDataTest])
def data_test_class(request):
    return request.param


class TestDataTestFeedback:
    """Tests for DataTest feedback generation."""

    def test_all_locales_have_same_data_test_feedback_keys(self):
        translator = Translator()

        locales = list(translator.data.keys())
        reference_locale = 'en'

        for test_type in ['table_data_test', 'view_data_test']:
            reference_keys = set(
                translator.data[reference_locale][test_type].keys()
            )

            for locale in locales:
                locale_keys = set(
                    translator.data[locale][test_type].keys()
                )

                assert locale_keys == reference_keys, (
                    f"Locale '{locale}' has different feedback keys "
                    f"for '{test_type}'. "
                    f"Missing: {reference_keys - locale_keys}. "
                    f"Extra: {locale_keys - reference_keys}."
                )

    # Result Existence tests - should exist
    def test_rows_should_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when table has results."""
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]

        test = data_test_class(
            name='users',
            title='rows_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'rows_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

        assert_feedback_translates_in_all_locales(result)

    def test_rows_should_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when table has no results."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            title='rows_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'rows_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when column has results."""
        mock_cursor.fetchall.return_value = [('value1',)]

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when column has no results."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_positive_feedback_none_and_other_values(self, mock_cursor, data_test_class):
        """Test positive feedback when column has results."""
        mock_cursor.fetchall.return_value = [('value1',), (None,)]

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_negative_feedback_only_none_values(self, mock_cursor, data_test_class):
        """Test negative feedback when column has no results."""
        mock_cursor.fetchall.return_value = [(None,), (None,)]

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_positive_feedback_with_count(self, mock_cursor, data_test_class):
        """Test negative feedback when COUNT(*) returns 0."""
        mock_cursor.fetchall.return_value = [(1,)]

        test = data_test_class(
            name='users',
            column_name='COUNT(*)',
            title='column_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'COUNT(*)'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_exist_negative_feedback_with_count(self, mock_cursor, data_test_class):
        """Test negative feedback when COUNT(*) returns 0."""
        mock_cursor.fetchall.return_value = [(0,)]

        test = data_test_class(
            name='users',
            column_name='COUNT(*)',
            title='column_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'COUNT(*)'

        assert_feedback_translates_in_all_locales(result)

    # Result Existence tests - should NOT exist
    def test_rows_should_not_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when table has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='deleted_users',
            should_exist=False,
            title='rows_should_not_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'rows_should_not_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'deleted_users'

        assert_feedback_translates_in_all_locales(result)

    def test_rows_should_not_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when table has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('result1',)]

        test = data_test_class(
            name='users',
            should_exist=False,
            title='rows_should_not_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'rows_should_not_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_not_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when column has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='deleted_at',
            should_exist=False,
            title='column_value_should_not_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_value_should_not_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'deleted_at'

        assert_feedback_translates_in_all_locales(result)

    def test_column_value_should_not_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when column has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('value1',)]

        test = data_test_class(
            name='users',
            column_name='name',
            should_exist=False,
            title='column_value_should_not_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_value_should_not_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

        assert_feedback_translates_in_all_locales(result)

    # Single expected value tests
    def test_expected_value_should_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when expected value is found."""
        mock_cursor.fetchall.return_value = [('John',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            title='expected_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'John'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_should_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            title='expected_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'John'
        assert result['message']['params']['actual_value'] == 'Jane'

        assert_feedback_translates_in_all_locales(result)

    def test_test_query_returned_more_rows_than_expected(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',), ('John',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            title='test_query_returned_more_rows_than_expected',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'test_query_returned_more_rows_than_expected'
        assert result['message']['params']['unexpected_row_count'] == 2

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_should_exist_positive_feedback_none_value(self, mock_cursor, data_test_class):
        """Test positive feedback when expected value is found."""
        mock_cursor.fetchall.return_value = [(None,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='NULL',
            title='expected_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'NULL'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_should_exist_negative_feedback_none_value(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='NULL',
            title='expected_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'NULL'
        assert result['message']['params']['actual_value'] == 'Jane'

        assert_feedback_translates_in_all_locales(result)

    # Single expected values should NOT exist
    def test_expected_value_should_not_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when expected value is not found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('Jane',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            should_exist=False,
            title='expected_value_should_not_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_should_not_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'John'
        assert result['message']['params']['actual_value'] == 'Jane'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_should_not_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('John',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            should_exist=False,
            title='expected_value_should_not_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_not_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_value'] == 'John'

        assert_feedback_translates_in_all_locales(result)

    # Expected value range tests
    def test_expected_value_range_positive_feedback_min_value(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.return_value = [(1,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='expected_value_range_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_range_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == 1

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_range_positive_feedback_max_value(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.return_value = [(10,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='expected_value_range_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_range_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == 10

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_range_negative_feedback_below_min(self, mock_cursor, data_test_class):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.return_value = [(-5,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='expected_value_range_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_range_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == -5

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_range_negative_feedback_over_max(self, mock_cursor, data_test_class):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.return_value = [(15,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='expected_value_range_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_range_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == 15

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_positive_feedback_not_allow_extra_values_float_in_range(self, mock_cursor,
                                                                                              data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [(2.50000001,)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=[1, 2.6],
            title='expected_values_group_positive_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        print(result)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_range_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'

        assert_feedback_translates_in_all_locales(result)

    def test_test_query_returned_no_rows(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='test_query_returned_no_rows',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'test_query_returned_no_rows'

        assert_feedback_translates_in_all_locales(result)

    def test_test_query_returned_more_rows_than_expected(self, mock_cursor, data_test_class):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',), ('John',)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 10],
            title='test_query_returned_more_rows_than_expected',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'test_query_returned_more_rows_than_expected'
        assert result['message']['params']['unexpected_row_count'] == 2

        assert_feedback_translates_in_all_locales(result)

    # Expected value group tests
    def test_expected_values_group_positive_feedback_allow_extra_values_strings(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',), ('pending',), ('testing',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_positive_feedback',
            allow_extra_values=True,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_values_group_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_negative_feedback_allow_extra_values_strings(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',), ('testing',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_missing_negative_feedback',
            allow_extra_values=True,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_values_group_missing_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['expected_values'] == ['pending']

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_positive_feedback_not_allow_extra_values(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',), ('pending',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_positive_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_values_group_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_missing_negative_feedback_not_allow_extra_values(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_missing_negative_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_values_group_missing_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'
        assert result['message']['params']['expected_values'] == ['pending']

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_unexpected_negative_feedback_not_allow_extra_values(self, mock_cursor,
                                                                                       data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',), ('pending',), ('testing',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_unexpected_negative_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_values_group_unexpected_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'
        assert result['message']['params']['unexpected_values'] == ['testing']

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_missing_and_unexpected_negative_feedback_not_allow_extra_values(self, mock_cursor,
                                                                                                   data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [('active',), ('inactive',), ('testing',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_values_group_missing_and_unexpected_negative_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_values_group_missing_and_unexpected_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'
        assert result['message']['params']['expected_values'] == ['pending']
        assert result['message']['params']['unexpected_values'] == ['testing']

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_positive_feedback_allow_extra_values_numbers(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=[1, 2, 3],
            title='expected_values_group_positive_feedback',
            allow_extra_values=True,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_values_group_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'

        assert_feedback_translates_in_all_locales(result)

    def test_expected_values_group_negative_feedback_allow_extra_values_numbers(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.return_value = [(1,), (2,), (4,)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=[1, 2, 3],
            title='expected_values_group_missing_negative_feedback',
            allow_extra_values=True,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_values_group_missing_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['expected_values'] == [3]

        assert_feedback_translates_in_all_locales(result)

    def test_expected_value_should_exist_no_result_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when no result is found for expected value."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 999",
            expected_value='John',
            title='expected_value_should_exist_no_result_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'test_query_returned_no_rows'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['expected_value'] == 'John'

        assert_feedback_translates_in_all_locales(result)

    # Expected value group tests for float values and numeric tolerance #33
    def test_expected_values_group_positive_feedback_not_allow_extra_values_float_values(self, mock_cursor,
                                                                                         data_test_class):
        """Test positive feedback when value is in string list and extra values are allowed"""
        mock_cursor.fetchall.return_value = [(1,), (2.5,), (3,)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=[1, 2.5, 3],
            title='expected_values_group_positive_feedback',
            allow_extra_values=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_values_group_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'status'

        assert_feedback_translates_in_all_locales(result)

    def test_legacy_is_view_still_works(self, mock_cursor):
        mock_cursor.fetchall.return_value = [('result1',)]

        test = DataTest(
            name='user_view',
            isView=True,
            points=10
        )

        result = test.run(mock_cursor)

        assert result['message']['test_type'] == 'view_data_test'


def assert_feedback_translates_in_all_locales(result):
    translator = Translator()

    for locale in translator.data.keys():
        translator.set_locale(locale)

        feedback = translator.translate(
            result['message']['test_type'],
            result['message']['test_key'],
            **result['message']['params']
        )

        assert "not supported" not in feedback.lower()
        assert "$" not in feedback, (
            f"Unresolved parameter in locale '{locale}': {feedback}"
        )
