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

    def test_not_expected_value_should_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when table has results."""
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]

        test = data_test_class(
            name='users',
            title='not_expected_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'not_expected_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

    def test_not_expected_value_should_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when table has no results."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            title='not_expected_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'not_expected_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

    def test_column_not_expected_value_should_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when column has results."""
        mock_cursor.fetchall.return_value = [('value1',)]

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_not_expected_value_should_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_not_expected_value_should_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

    def test_column_not_expected_value_should_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when column has no results."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='name',
            title='column_not_expected_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == data_test_class.test_type
        assert result['message']['test_key'] == 'column_not_expected_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'

    def test_column_not_expected_value_should_exist_negative_feedback_with_count(self, mock_cursor, data_test_class):
        """Test negative feedback when COUNT(*) returns 0."""
        mock_cursor.fetchall.return_value = [(0,)]

        test = data_test_class(
            name='users',
            column_name='COUNT(*)',
            title='column_not_expected_value_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_not_expected_value_should_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'COUNT(*)'

    def test_not_expected_value_should_not_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when table has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='deleted_users',
            should_exist=False,
            title='not_expected_value_should_not_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'not_expected_value_should_not_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'deleted_users'

    def test_not_expected_value_should_not_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when table has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('result1',)]

        test = data_test_class(
            name='users',
            should_exist=False,
            title='not_expected_value_should_not_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'not_expected_value_should_not_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

    def test_column_not_expected_value_should_not_exist_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when column has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []

        test = data_test_class(
            name='users',
            column_name='deleted_at',
            should_exist=False,
            title='column_not_expected_value_should_not_exist_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_not_expected_value_should_not_exist_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'deleted_at'

    def test_table_column_not_expected_value_should_not_exist_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when column has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('value1',)]

        test = data_test_class(
            name='users',
            column_name='name',
            should_exist=False,
            title='column_not_expected_value_should_not_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_not_expected_value_should_not_exist_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'


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

    def test_expected_value_group_numbers_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.return_value = [(5,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='expected_value_group_numbers_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_group_numbers_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == 5

    def test_expected_value_group_numbers_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.return_value = [(15,)]

        test = data_test_class(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='expected_value_group_numbers_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_group_numbers_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'
        assert result['message']['params']['column_name'] == 'name'
        assert result['message']['params']['expected_min_value'] == 1
        assert result['message']['params']['expected_max_value'] == 10
        assert result['message']['params']['actual_value'] == 15

    def test_expected_value_group_strings_positive_feedback(self, mock_cursor, data_test_class):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.return_value = [('active', 'inactive', 'pending')]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='expected_value_group_strings_positive_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_group_strings_positive_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

    def test_expected_value_group_strings_negative_feedback(self, mock_cursor, data_test_class):
        """Test negative feedback when value is not in string list."""
        mock_cursor.fetchall.return_value = [('deleted',)]

        test = data_test_class(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='table_expected_value_group_strings_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_group_strings_negative_feedback'
        assert result['message']['params'][data_test_class.name_parameter] == 'users'

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


def test_legacy_is_view_still_works(mock_cursor):
    mock_cursor.fetchall.return_value = [('result1',)]

    test = DataTest(
        name='user_view',
        isView=True,
        points=10
    )

    result = test.run(mock_cursor)

    assert result['message']['test_type'] == 'view_data_test'
