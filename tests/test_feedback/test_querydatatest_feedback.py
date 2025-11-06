"""
Tests for QueryDataTest feedback messages.
Tests all feedback keys from the query_data_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.QueryDataTest import QueryDataTest


class TestQueryDataTestFeedback:
    """Tests for QueryDataTest feedback generation."""

    def test_query_not_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when query has results."""
        mock_cursor.fetchall.return_value = [('result1',), ('result2',)]
        
        test = QueryDataTest(
            name='query_test',
            title='query_not_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'query_data_test'
        assert result['message']['test_key'] == 'query_not_expected_value_should_exist_positive_feedback'

    def test_query_not_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when query has no results."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            title='query_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_not_expected_value_should_exist_negative_feedback'

    def test_query_column_not_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when query column has results."""
        mock_cursor.fetchall.return_value = [('value1',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            title='query_column_not_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_column_not_expected_value_should_exist_positive_feedback'
        assert 'name' in result['message']['params']

    def test_query_column_not_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when query column has no results."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            title='query_column_not_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_column_not_expected_value_should_exist_negative_feedback'

    def test_query_not_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when query has no results (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            should_exist=False,
            title='query_not_expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_not_expected_value_should_not_exist_positive_feedback'

    def test_query_not_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when query has results (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('result1',)]
        
        test = QueryDataTest(
            name='query_test',
            should_exist=False,
            title='query_not_expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_not_expected_value_should_not_exist_negative_feedback'

    def test_query_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value is found."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            where="test_id = 1",
            expected_value='John',
            title='query_expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_expected_value_should_exist_positive_feedback'
        assert 'John' in result['message']['params']

    def test_query_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value is not found."""
        mock_cursor.fetchall.return_value = [('Jane',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            where="test_id = 1",
            expected_value='John',
            title='query_expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_should_exist_negative_feedback'
        assert 'John' in result['message']['params']
        assert 'Jane' in result['message']['params']

    def test_query_expected_value_should_exist_no_result_negative_feedback(self, mock_cursor):
        """Test negative feedback when no result found for expected value."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            where="test_id = 999",
            expected_value='John',
            title='query_expected_value_should_exist_no_result_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_should_exist_no_result_negative_feedback'

    def test_query_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value is not found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('Jane',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            where="test_id = 1",
            expected_value='John',
            should_exist=False,
            title='query_expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_expected_value_should_not_exist_positive_feedback'

    def test_query_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value is found (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            where="test_id = 1",
            expected_value='John',
            should_exist=False,
            title='query_expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_should_not_exist_negative_feedback'

    def test_query_expected_value_group_numbers_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.return_value = [(5,)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='price',
            where="test_id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='query_expected_value_group_numbers_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_expected_value_group_numbers_positive_feedback'

    def test_query_expected_value_group_numbers_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.return_value = [(15,)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='price',
            where="test_id = 1",
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='query_expected_value_group_numbers_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_group_numbers_negative_feedback'

    def test_query_expected_value_group_numbers_no_result_negative_feedback(self, mock_cursor):
        """Test negative feedback when no result for number range check."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            column_name='price',
            where="test_id = 999",
            expected_value=[1, 2, 3, 4, 5],
            title='query_expected_value_group_numbers_no_result_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_group_numbers_no_result_negative_feedback'

    def test_query_expected_value_group_strings_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.return_value = [('active',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='status',
            where="test_id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='query_expected_value_group_strings_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_expected_value_group_strings_positive_feedback'

    def test_query_expected_value_group_strings_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in string list."""
        mock_cursor.fetchall.return_value = [('deleted',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='status',
            where="test_id = 1",
            expected_value=['active', 'inactive', 'pending'],
            title='query_expected_value_group_strings_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_expected_value_group_strings_negative_feedback'

    def test_query_no_result(self, mock_cursor):
        """Test query_no_result feedback."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryDataTest(
            name='query_test',
            column_name='COUNT(*)',
            title='query_no_result',
            points=10
        )
        
        result = test.run(mock_cursor)
        # This tests the scenario where COUNT(*) returns 0
        assert result['is_success'] is False

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('John',)]
        
        test = QueryDataTest(
            name='query_test',
            column_name='name',
            expected_value='John',
            custom_feedback='Custom query test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom query test message' in result['message']['params']

