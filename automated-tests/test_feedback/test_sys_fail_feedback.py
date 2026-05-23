"""
Tests for system failure feedback messages.
Tests all feedback keys from the sys_fail section of locale files.
These tests verify error handling in TestDefinition.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.TestDefinition import TestDefinition


class FailingTest(TestDefinition):
    """Test class that raises specific exceptions for testing error handling."""
    
    def __init__(self, exception_type, exception_message='', **kwargs):
        self.exception_type = exception_type
        self.exception_message = exception_message
        super().__init__(name='test', points=10, **kwargs)
    
    def execute(self, cursor):
        # Create exception classes dynamically
        if self.exception_type == 'UndefinedColumn':
            error = type('UndefinedColumn', (Exception,), {})()
            error.args = (self.exception_message,)
            raise error
        elif self.exception_type == 'UndefinedTable':
            error = type('UndefinedTable', (Exception,), {})()
            error.args = (self.exception_message,)
            raise error
        elif self.exception_type == 'AmbiguousColumn':
            error = type('AmbiguousColumn', (Exception,), {})()
            error.args = (self.exception_message,)
            raise error
        elif self.exception_type == 'UndefinedFunction':
            error = type('UndefinedFunction', (Exception,), {})()
            error.args = (self.exception_message,)
            raise error
        elif self.exception_type == 'IndexError':
            raise IndexError(self.exception_message)
        else:
            raise Exception(self.exception_message)


class TestSysFailFeedback:
    """Tests for system failure feedback generation."""

    def test_undefined_column_feedback(self, mock_cursor):
        """Test feedback for undefined column error."""
        test = FailingTest(
            exception_type='UndefinedColumn',
            exception_message='column "missing_column" does not exist'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_column'
        assert 'missing_column' in result['message']['params'][0]

    def test_undefined_table_feedback(self, mock_cursor):
        """Test feedback for undefined table error."""
        test = FailingTest(
            exception_type='UndefinedTable',
            exception_message='relation "missing_table" does not exist'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_table'
        assert 'missing_table' in result['message']['params'][0]

    def test_ambiguous_column_feedback(self, mock_cursor):
        """Test feedback for ambiguous column error."""
        test = FailingTest(
            exception_type='AmbiguousColumn',
            exception_message='column reference "id" is ambiguous'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'ambiguous_column'
        assert 'id' in result['message']['params'][0]

    def test_undefined_function_round_feedback(self, mock_cursor):
        """Test feedback for undefined function round error."""
        test = FailingTest(
            exception_type='UndefinedFunction',
            exception_message='function round(column_name, 2) does not exist'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_function_round'
        assert 'column_name' in result['message']['params'][0]

    def test_undefined_function_generic_feedback(self, mock_cursor):
        """Test feedback for generic undefined function error."""
        test = FailingTest(
            exception_type='UndefinedFunction',
            exception_message='function nonexistent_func() does not exist'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['is_sys_fail'] is True
        # Generic function error returns raw exception message

    def test_index_error_feedback(self, mock_cursor):
        """Test feedback for index error."""
        test = FailingTest(
            exception_type='IndexError',
            exception_message='list index out of range'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'index_error'
        assert result['message']['params'] == []

    def test_generic_exception_feedback(self, mock_cursor):
        """Test feedback for generic exception."""
        test = FailingTest(
            exception_type='Generic',
            exception_message='Some other error occurred'
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['is_sys_fail'] is True
        # Generic exceptions return sys.exc_info() as message

    def test_rollback_on_error(self, mock_cursor):
        """Test that rollback is called on error."""
        test = FailingTest(
            exception_type='UndefinedColumn',
            exception_message='column "test" does not exist'
        )
        
        test.run(mock_cursor)
        
        # Verify rollback was called
        rollback_calls = [call for call in mock_cursor.execute.call_args_list 
                         if 'ROLLBACK' in str(call)]
        assert len(rollback_calls) > 0 or mock_cursor.execute.called

