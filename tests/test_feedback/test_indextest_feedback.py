"""
Tests for IndexTest feedback messages.
Tests all feedback keys from the index_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.IndexTest import IndexTest


class TestIndexTestFeedback:
    """Tests for IndexTest feedback generation."""

    def test_index_positive_feedback(self, mock_cursor):
        """Test positive feedback when index exists."""
        mock_cursor.fetchall.return_value = [('idx_users_email', 'users', 'email')]
        
        test = IndexTest(
            name='idx_users_email',
            title='index_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'index_test'
        assert result['message']['test_key'] == 'index_positive_feedback'
        assert 'idx_users_email' in result['message']['params']

    def test_index_negative_feedback(self, mock_cursor):
        """Test negative feedback when index does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = IndexTest(
            name='nonexistent_index',
            title='index_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'index_negative_feedback'
        assert 'nonexistent_index' in result['message']['params']

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('idx_users_email', 'users', 'email')]
        
        test = IndexTest(
            name='idx_users_email',
            custom_feedback='Custom index test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom index test message' in result['message']['params']

