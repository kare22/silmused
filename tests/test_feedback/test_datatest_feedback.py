"""
Tests for DataTest feedback messages.
Tests all feedback keys from the data_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.DataTest import DataTest
from silmused.Translator import Translator


class TestDataTestFeedback:
    """Tests for DataTest feedback generation."""

    def test_table_not_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when table has results."""
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
        
        test = DataTest(
            name='users',
            title='table_not_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'data_test'
        assert result['message']['test_key'] == 'table_not_expected_value_should_exist_positive_feedback'
        assert 'users' in result['message']['params']

    def test_table_not_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when table has no results."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='users',
            title='table_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'data_test'
        assert result['message']['test_key'] == 'table_not_expected_value_should_exist_negative_feedback'
        assert 'users' in result['message']['params']

    def test_table_column_not_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column has results."""
        mock_cursor.fetchall.return_value = [('value1',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            title='table_column_not_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'data_test'
        assert result['message']['test_key'] == 'table_column_not_expected_value_should_exist_positive_feedback'
        assert 'users' in result['message']['params']
        assert 'name' in result['message']['params']

    def test_table_column_not_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column has no results."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='users',
            column_name='name',
            title='table_column_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'data_test'
        assert result['message']['test_key'] == 'table_column_not_expected_value_should_exist_negative_feedback'

    def test_table_column_not_expected_value_should_exist_negative_feedback_with_count(self, mock_cursor):
        """Test negative feedback when COUNT(*) returns 0."""
        mock_cursor.fetchall.return_value = [(0,)]
        
        test = DataTest(
            name='users',
            column_name='COUNT(*)',
            title='table_column_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_not_expected_value_should_exist_negative_feedback'

    def test_table_not_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when table has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='deleted_users',
            should_exist=False,
            title='table_not_expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_not_expected_value_should_not_exist_positive_feedback'

    def test_table_not_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when table has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('result1',)]
        
        test = DataTest(
            name='users',
            should_exist=False,
            title='table_not_expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_not_expected_value_should_not_exist_negative_feedback'

    def test_table_column_not_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='users',
            column_name='deleted_at',
            should_exist=False,
            title='table_column_not_expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_not_expected_value_should_not_exist_positive_feedback'

    def test_table_column_not_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('value1',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            should_exist=False,
            title='table_column_not_expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_not_expected_value_should_not_exist_negative_feedback'

    def test_table_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value is found."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            title='table_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_expected_value_should_exist_positive_feedback'
        assert 'John' in result['message']['params']
        assert 'users' in result['message']['params']

    def test_table_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            title='table_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_should_exist_negative_feedback'
        assert 'John' in result['message']['params']
        assert 'Jane' in result['message']['params']

    def test_table_expected_value_should_exist_no_result_negative_feedback(self, mock_cursor):
        """Test negative feedback when no result is found for expected value."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='users',
            column_name='name',
            where="id = 999",
            expected_value='John',
            title='table_expected_value_should_exist_no_result_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_should_exist_no_result_negative_feedback'

    def test_table_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value is not found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('Jane',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            should_exist=False,
            title='table_expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_expected_value_should_not_exist_positive_feedback'

    def test_table_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value is found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            where="id = 1",
            expected_value='John',
            should_exist=False,
            title='table_expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_should_not_exist_negative_feedback'

    def test_table_expected_value_group_numbers_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.return_value = [(5,)]
        
        test = DataTest(
            name='products',
            column_name='price',
            where="id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='table_expected_value_group_numbers_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_expected_value_group_numbers_positive_feedback'

    def test_table_expected_value_group_numbers_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.return_value = [(15,)]
        
        test = DataTest(
            name='products',
            column_name='price',
            where="id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='table_expected_value_group_numbers_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_group_numbers_negative_feedback'

    def test_table_expected_value_group_numbers_no_result_negative_feedback(self, mock_cursor):
        """Test negative feedback when no result for number range check."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='products',
            column_name='price',
            where="id = 999",
            expected_value=[1, 2, 3, 4, 5],
            title='table_expected_value_group_numbers_no_result_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_group_numbers_no_result_negative_feedback'

    def test_table_expected_value_group_strings_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.return_value = [('active',)]
        
        test = DataTest(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='table_expected_value_group_strings_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_expected_value_group_strings_positive_feedback'

    def test_table_expected_value_group_strings_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in string list."""
        mock_cursor.fetchall.return_value = [('deleted',)]
        
        test = DataTest(
            name='users',
            column_name='status',
            where="id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='table_expected_value_group_strings_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_expected_value_group_strings_negative_feedback'

    def test_view_not_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when view has results."""
        mock_cursor.fetchall.return_value = [('result1',)]
        
        test = DataTest(
            name='user_view',
            isView=True,
            title='view_not_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'view_not_expected_value_should_exist_positive_feedback'

    def test_view_not_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when view has no results."""
        mock_cursor.fetchall.return_value = []
        
        test = DataTest(
            name='user_view',
            isView=True,
            title='view_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'view_not_expected_value_should_exist_negative_feedback'

    def test_view_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value found in view."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = DataTest(
            name='user_view',
            column_name='name',
            where="id = 1",
            expected_value='John',
            isView=True,
            title='view_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'view_expected_value_should_exist_positive_feedback'

    def test_view_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value not found in view."""
        mock_cursor.fetchall.return_value = [('Jane',)]
        
        test = DataTest(
            name='user_view',
            column_name='name',
            where="id = 1",
            expected_value='John',
            isView=True,
            title='view_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'view_expected_value_should_exist_negative_feedback'

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = DataTest(
            name='users',
            column_name='name',
            expected_value='John',
            custom_feedback='Custom message here',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom message here' in result['message']['params']

