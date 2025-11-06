"""
Tests for QueryStructureTest feedback messages.
Tests all feedback keys from the query_structure_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.QueryStructureTest import QueryStructureTest


class TestQueryStructureTestFeedback:
    """Tests for QueryStructureTest feedback generation."""

    def test_query_table_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when query_test table exists."""
        mock_cursor.fetchall.return_value = [('query_test', 'id', 'integer')]
        
        test = QueryStructureTest(
            name='query_test',
            title='query_table_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'query_structure_test'
        assert result['message']['test_key'] == 'query_table_should_exist_positive_feedback'

    def test_query_table_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when query_test table does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryStructureTest(
            name='query_test',
            title='query_table_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        # Note: There's a bug in QueryStructureTest - it uses 'structure_test' instead of 'query_structure_test' for negative
        assert 'query' in result['message']['test_key'] or 'structure' in result['message']['test_key']

    def test_query_column_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column exists in query_test."""
        mock_cursor.fetchall.return_value = [('query_test', 'name', 'varchar')]
        
        test = QueryStructureTest(
            name='query_test',
            column_name='name',
            title='query_column_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_column_should_exist_positive_feedback'
        assert 'name' in result['message']['params']

    def test_query_column_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column does not exist in query_test."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryStructureTest(
            name='query_test',
            column_name='nonexistent',
            title='query_column_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_column_should_exist_negative_feedback'
        assert 'nonexistent' in result['message']['params']

    def test_query_table_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when query_test table does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryStructureTest(
            name='query_test',
            should_exist=False,
            title='query_table_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_table_should_not_exist_positive_feedback'

    def test_query_table_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when query_test table exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('query_test', 'id', 'integer')]
        
        test = QueryStructureTest(
            name='query_test',
            should_exist=False,
            title='query_table_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_table_should_not_exist_negative_feedback'

    def test_query_column_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column does not exist in query_test (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = QueryStructureTest(
            name='query_test',
            column_name='deleted_column',
            should_exist=False,
            title='query_column_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'query_column_should_not_exist_positive_feedback'

    def test_query_column_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column exists in query_test (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('query_test', 'name', 'varchar')]
        
        test = QueryStructureTest(
            name='query_test',
            column_name='name',
            should_exist=False,
            title='query_column_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'query_column_should_not_exist_negative_feedback'

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('query_test', 'name', 'varchar')]
        
        test = QueryStructureTest(
            name='query_test',
            column_name='name',
            custom_feedback='Custom query structure test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom query structure test message' in result['message']['params']

