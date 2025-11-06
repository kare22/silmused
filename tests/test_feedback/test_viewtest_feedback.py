"""
Tests for ViewTest feedback messages.
Tests all feedback keys from the view_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.ViewTest import ViewTest


class TestViewTestFeedback:
    """Tests for ViewTest feedback generation."""

    def test_view_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when view exists."""
        mock_cursor.fetchall.return_value = [('user_view', 'id', 'integer')]
        
        test = ViewTest(
            name='user_view',
            title='view_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'view_test'
        assert result['message']['test_key'] == 'view_should_exist_positive_feedback'
        assert 'user_view' in result['message']['params']

    def test_view_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when view does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='nonexistent_view',
            title='view_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'view_should_exist_negative_feedback'

    def test_column_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column exists in view."""
        mock_cursor.fetchall.return_value = [('user_view', 'name', 'varchar')]
        
        test = ViewTest(
            name='user_view',
            column_name='name',
            title='column_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_should_exist_positive_feedback'
        assert 'name' in result['message']['params']
        assert 'user_view' in result['message']['params']

    def test_column_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column does not exist in view."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='user_view',
            column_name='nonexistent',
            title='column_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_should_exist_negative_feedback'

    def test_view_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when view does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='deleted_view',
            should_exist=False,
            title='view_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'view_should_not_exist_positive_feedback'

    def test_view_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when view exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('user_view', 'id', 'integer')]
        
        test = ViewTest(
            name='user_view',
            should_exist=False,
            title='view_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'view_should_not_exist_negative_feedback'

    def test_column_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column does not exist in view (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='user_view',
            column_name='deleted_column',
            should_exist=False,
            title='column_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_should_not_exist_positive_feedback'

    def test_column_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column exists in view (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('user_view', 'name', 'varchar')]
        
        test = ViewTest(
            name='user_view',
            column_name='name',
            should_exist=False,
            title='column_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_should_not_exist_negative_feedback'

    def test_mat_view_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when materialized view exists."""
        mock_cursor.fetchall.return_value = [('user_mat_view',)]
        
        test = ViewTest(
            name='user_mat_view',
            isMaterialized=True,
            title='mat_view_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'mat_view_should_exist_positive_feedback'

    def test_mat_view_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when materialized view does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='nonexistent_mat_view',
            isMaterialized=True,
            title='mat_view_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'mat_view_should_exist_negative_feedback'

    def test_mat_view_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when materialized view does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ViewTest(
            name='deleted_mat_view',
            isMaterialized=True,
            should_exist=False,
            title='mat_view_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'mat_view_should_not_exist_positive_feedback'

    def test_mat_view_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when materialized view exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('user_mat_view',)]
        
        test = ViewTest(
            name='user_mat_view',
            isMaterialized=True,
            should_exist=False,
            title='mat_view_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'mat_view_should_not_exist_negative_feedback'

    def test_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value matches."""
        mock_cursor.fetchall.return_value = [(80,)]
        
        test = ViewTest(
            name='user_view',
            expected_value=80,
            title='expected_value_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_should_exist_positive_feedback'

    def test_expected_value_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value does not match."""
        mock_cursor.fetchall.return_value = [(100,)]
        
        test = ViewTest(
            name='user_view',
            expected_value=80,
            title='expected_value_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_exist_negative_feedback'

    def test_expected_value_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = [(100,)]  # Different value
        
        test = ViewTest(
            name='user_view',
            expected_value=80,
            should_exist=False,
            title='expected_value_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'expected_value_should_not_exist_positive_feedback'

    def test_expected_value_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [(80,)]  # Same value
        
        test = ViewTest(
            name='user_view',
            expected_value=80,
            should_exist=False,
            title='expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_not_exist_negative_feedback'

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('user_view', 'id', 'integer')]
        
        test = ViewTest(
            name='user_view',
            custom_feedback='Custom view test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom view test message' in result['message']['params']

