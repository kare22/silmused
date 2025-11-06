"""
Tests for TriggerTest feedback messages.
Tests all feedback keys from the trigger_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.TriggerTest import TriggerTest


class TestTriggerTestFeedback:
    """Tests for TriggerTest feedback generation."""

    def test_trigger_exists_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger exists."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
            [('trg_users_updated',)],  # Manipulation check (if arguments provided)
            [('trg_users_updated',)]  # Action timing check (if provided)
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=[],
            title='trigger_exists_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        # Trigger exists check happens first
        assert result is not None
        # If trigger exists, we continue to definition check
        # If it doesn't exist, we get trigger_exists_negative_feedback

    def test_trigger_exists_negative_feedback(self, mock_cursor):
        """Test negative feedback when trigger does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = TriggerTest(
            name='nonexistent_trigger',
            arguments=[],
            title='trigger_exists_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'trigger_test'
        assert result['message']['test_key'] == 'trigger_exists_negative_feedback'
        assert 'nonexistent_trigger' in result['message']['params']

    def test_trigger_definition_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger definition is correct."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
            [('trg_users_updated',)],  # UPDATE manipulation found
            [('trg_users_updated',)]  # BEFORE timing found
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=['UPDATE'],
            action_timing='BEFORE',
            title='trigger_definition_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'trigger_definition_positive_feedback'
        assert 'trg_users_updated' in result['message']['params']

    def test_trigger_definition_negative_feedback(self, mock_cursor):
        """Test negative feedback when trigger definition has errors."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
            [],  # UPDATE manipulation not found
            [('trg_users_updated',)]  # BEFORE timing found
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=['UPDATE'],
            action_timing='BEFORE',
            title='trigger_definition_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_definition_negative_feedback'
        assert 'trg_users_updated' in result['message']['params']
        # Error details should be in params
        assert len(result['message']['params']) >= 2

    def test_trigger_definition_negative_feedback_missing_timing(self, mock_cursor):
        """Test negative feedback when action timing is incorrect."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
            [('trg_users_updated',)],  # UPDATE manipulation found
            []  # BEFORE timing not found
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=['UPDATE'],
            action_timing='BEFORE',
            title='trigger_definition_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_definition_negative_feedback'

    def test_trigger_definition_negative_feedback_multiple_errors(self, mock_cursor):
        """Test negative feedback when multiple definition errors exist."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
            [],  # UPDATE manipulation not found
            []  # BEFORE timing not found
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=['UPDATE'],
            action_timing='BEFORE',
            title='trigger_definition_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_definition_negative_feedback'
        # Should have multiple errors in params

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],
            [('trg_users_updated',)],
            [('trg_users_updated',)]
        ]
        
        test = TriggerTest(
            name='trg_users_updated',
            arguments=['UPDATE'],
            action_timing='BEFORE',
            custom_feedback='Custom trigger test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom trigger test message' in result['message']['params']

