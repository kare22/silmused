"""
Tests for TriggerTest feedback messages.
Tests all feedback keys from the trigger_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.TriggerTest import TriggerTest


class TestTriggerTestFeedback:
    """Tests for TriggerTest feedback generation."""

    def test_trigger_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger exists."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],
        ]
        test = TriggerTest(
            name='trg_users_updated',
            title='trigger_should_exist_positive_feedback',
            points=10,
        )

        result = test.run(mock_cursor)
        # Trigger exists check happens first
        assert result is not None
        assert result['is_success'] is True
        # Check for feedback message parameters
        assert result['message']['test_type'] == 'trigger_test'
        assert result['message']['test_key'] == 'trigger_should_exist_positive_feedback'
        assert 'trigger_name' in result['message']['params']
        assert result['message']['params']['trigger_name'] == 'trg_users_updated'

    def test_trigger_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when trigger does not exist."""
        mock_cursor.fetchall.return_value = []

        test = TriggerTest(
            name='nonexistent_trigger',
            title='trigger_should_exist_negative_feedback',
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'trigger_test'
        assert result['message']['test_key'] == 'trigger_should_exist_negative_feedback'
        assert 'nonexistent_trigger' in result['message']['params']['trigger_name']

    def test_trigger_should_not_exist_positive_feedback(self, mock_cursor):
        """Test negative feedback when trigger does not exist."""
        mock_cursor.fetchall.return_value = []

        test = TriggerTest(
            name='nonexistent_trigger',
            title='trigger_should_exist_negative_feedback',
            should_exist=False,
            points=10
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'trigger_test'
        assert result['message']['test_key'] == 'trigger_should_not_exist_positive_feedback'
        assert 'nonexistent_trigger' in result['message']['params']['trigger_name']

    def test_trigger_should_not_exist_negative_feedback(self, mock_cursor):
        """Test positive feedback when trigger exists."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],
        ]
        test = TriggerTest(
            name='trg_users_updated',
            title='trigger_should_exist_positive_feedback',
            should_exist=False,
            points=10,
        )

        result = test.run(mock_cursor)
        # Trigger exists check happens first
        assert result is not None
        assert result['is_success'] is False
        # Check for feedback message parameters
        assert result['message']['test_type'] == 'trigger_test'
        assert result['message']['test_key'] == 'trigger_should_not_exist_negative_feedback'
        assert 'trigger_name' in result['message']['params']
        assert result['message']['params']['trigger_name'] == 'trg_users_updated'

    def test_trigger_should_exist_action_timing_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger's action timing is correct."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists with correct
        ]

        test = TriggerTest(
            name='trg_users_updated',
            action_timing='BEFORE',
            title='trigger_should_exist_action_timing_positive_feedback',
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'trigger_should_exist_action_timing_positive_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['action_timing']

    def test_trigger_should_exist_action_timing_negative_feedback(self, mock_cursor):
        """Test positive feedback when trigger's action timing is correct."""
        mock_cursor.fetchall.side_effect = [
            [],  # No such trigger found
        ]

        test = TriggerTest(
            name='trg_users_updated',
            action_timing='BEFORE',
            title='trigger_should_exist_action_timing_negative_feedback',
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_should_exist_action_timing_negative_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['action_timing']

    def test_trigger_should_not_exist_action_timing_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger's action timing is correct."""
        mock_cursor.fetchall.side_effect = [
            [],  # Trigger exists with correct
        ]

        test = TriggerTest(
            name='trg_users_updated',
            action_timing='BEFORE',
            title='trigger_should_not_exist_action_timing_positive_feedback',
            should_exist=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'trigger_should_not_exist_action_timing_positive_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['action_timing']

    def test_trigger_should_not_exist_action_timing_negative_feedback(self, mock_cursor):
        """Test negative feedback when trigger's action timing is incorrect."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists with incorrect action timing
        ]

        test = TriggerTest(
            name='trg_users_updated',
            action_timing='BEFORE',
            title='trigger_should_not_exist_action_timing_negative_feedback',
            should_exist=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_should_not_exist_action_timing_negative_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['action_timing']

    def test_trigger_should_exist_manipulation_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger's manipulation is correct."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
        ]

        test = TriggerTest(
            name='trg_users_updated',
            manipulation='BEFORE',
            title='trigger_should_exist_manipulation_positive_feedback',
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'trigger_should_exist_manipulation_positive_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['manipulation']

    def test_trigger_should_exist_manipulation_negative_feedback(self, mock_cursor):
        """Test positive feedback when trigger's manipulation is correct."""
        mock_cursor.fetchall.side_effect = [
            [],
        ]

        test = TriggerTest(
            name='trg_users_updated',
            manipulation='BEFORE',
            title='trigger_should_exist_manipulation_negative_feedback',
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_should_exist_manipulation_negative_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['manipulation']

    def test_trigger_should_not_exist_manipulation_positive_feedback(self, mock_cursor):
        """Test positive feedback when trigger's manipulation is correct."""
        mock_cursor.fetchall.side_effect = [
            [],
        ]

        test = TriggerTest(
            name='trg_users_updated',
            manipulation='BEFORE',
            title='trigger_should_not_exist_manipulation_positive_feedback',
            should_exist=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'trigger_should_not_exist_manipulation_positive_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['manipulation']

    def test_trigger_should_not_exist_manipulation_negative_feedback(self, mock_cursor):
        """Test positive feedback when trigger's manipulation is correct."""
        mock_cursor.fetchall.side_effect = [
            [('trg_users_updated',)],  # Trigger exists
        ]

        test = TriggerTest(
            name='trg_users_updated',
            manipulation='BEFORE',
            title='trigger_should_not_exist_manipulation_negative_feedback',
            should_exist=False,
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'trigger_should_not_exist_manipulation_negative_feedback'
        assert 'trg_users_updated' in result['message']['params']['trigger_name']
        assert 'BEFORE' in result['message']['params']['manipulation']

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
            points=10,
        )

        result = test.run(mock_cursor)
        assert result['message']['test_type'] == 'custom_feedback'
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom trigger test message' in result['message']['params']

    def test_trigger_debug_output(self, mock_cursor, capsys):
        # Arrange
        mock_cursor.fetchall.return_value = [('trg_users_updated',)]

        test = TriggerTest(
            name='trg_users_updated',
            title='debug_test',
            points=10,
            debug='DEBUG',  # enables print output
        )

        # Act
        test.run(mock_cursor)

        # Capture output
        captured = capsys.readouterr()

        # Assert
        assert "TRIGGER TEST DEBUG" in captured.out
        assert "trg_users_updated" in captured.out
        assert "FEEDBACK DEBUG" in captured.out

    def test_trigger_all_debug_output(self, mock_cursor, capsys):
        # Arrange
        mock_cursor.fetchall.return_value = [('trg_users_updated',)]

        test = TriggerTest(
            name='trg_users_updated',
            title='all_debug_test',
            points=10,
            debug='ALL',
        )

        # Act
        test.run(mock_cursor)

        # Capture output
        captured = capsys.readouterr()

        # Assert
        assert "TRIGGER TEST DEBUG" in captured.out
        assert "Test title: all_debug_test" in captured.out
        assert "name: trg_users_updated" in captured.out

    def test_trigger_llm_check(selfself, mock_cursor):
        mock_cursor.fetchall.return_value = [('trg_users_updated',)]

        test = TriggerTest(
            name='trg_users_updated',
            title='trigger_llm_check',
            points=10,
            llm_check=True,
            should_exist=False,
            debug='ALL'
        )

        # Act
        with pytest.raises(Exception) as exc_info:
            test.run(mock_cursor)

        # Exception result
        result = exc_info.value.args[0]

        # Assert
        assert result['test_type'] == 'sys_fail'
        assert result['test_key'] == 'llm_check_fail'
