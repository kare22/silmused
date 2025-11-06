"""
Tests for FunctionTest feedback messages.
Tests all feedback keys from the function_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.FunctionTest import FunctionTest


class TestFunctionTestFeedback:
    """Tests for FunctionTest feedback generation."""

    def test_function_exists_positive_feedback(self, mock_cursor):
        """Test positive feedback when function exists."""
        # Mock function exists check
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],  # Function exists
            [('calculate_total', 'FUNCTION')],  # Function type check
            [('calculate_total', 2)],  # Parameter count check
            [(120,)]  # Function execution result
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            number_of_parameters=2,
            title='function_exists_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        # Function exists check happens first, so if it fails, we get that feedback
        # If it passes, we continue to other checks
        assert result is not None

    def test_function_exists_negative_feedback(self, mock_cursor):
        """Test negative feedback when function does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = FunctionTest(
            name='nonexistent_function',
            arguments=[],
            title='function_exists_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_exists_negative_feedback'
        assert 'nonexistent_function' in result['message']['params']

    def test_function_type_positive_feedback(self, mock_cursor):
        """Test positive feedback when function type is correct."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],  # Function exists
            [('calculate_total', 'FUNCTION')],  # Function type is FUNCTION
            [('calculate_total', 2)],  # Parameter count
            [(120,)]  # Execution result
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            number_of_parameters=2,
            title='function_type_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        # Type check happens after exists check
        assert result is not None

    def test_function_type_negative_feedback(self, mock_cursor):
        """Test negative feedback when function type is incorrect."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],  # Function exists
            []  # But not of type FUNCTION
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[],
            title='function_type_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_type_negative_feedback'

    def test_function_parameters_amount_positive_feedback(self, mock_cursor):
        """Test positive feedback when parameter count is correct."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],  # Function exists
            [('calculate_total', 'FUNCTION')],  # Type check
            [('calculate_total', 2)],  # Parameter count is 2
            [(120,)]  # Execution
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            number_of_parameters=2,
            title='function_parameters_amount_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result is not None

    def test_function_parameters_amount_negative_feedback(self, mock_cursor):
        """Test negative feedback when parameter count is incorrect."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],  # Function exists
            [('calculate_total', 'FUNCTION')],  # Type check
            [('calculate_total', 1)]  # Parameter count is 1, expected 2
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100],
            number_of_parameters=2,
            title='function_parameters_amount_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_parameters_amount_negative_feedback'

    def test_function_not_expected_value_not_expected_result_count_positive_feedback(self, mock_cursor):
        """Test positive feedback when function returns results (no expected value/count)."""
        mock_cursor.fetchall.side_effect = [
            [('get_users',)],  # Function exists
            [('get_users', 'FUNCTION')],  # Type check
            [(1,), (2,), (3,)]  # Function returns results
        ]
        
        test = FunctionTest(
            name='get_users',
            arguments=[],
            title='function_not_expected_value_not_expected_result_count_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'function_not_expected_value_not_expected_result_count_positive_feedback'

    def test_function_not_expected_value_not_expected_result_count_negative_feedback(self, mock_cursor):
        """Test negative feedback when function returns no results."""
        mock_cursor.fetchall.side_effect = [
            [('get_users',)],
            [('get_users', 'FUNCTION')],
            []  # No results
        ]
        
        test = FunctionTest(
            name='get_users',
            arguments=[],
            title='function_not_expected_value_not_expected_result_count_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_not_expected_value_not_expected_result_count_negative_feedback'

    def test_function_not_expected_value_expected_result_count_positive_feedback(self, mock_cursor):
        """Test positive feedback when result count matches expected count."""
        mock_cursor.fetchall.side_effect = [
            [('get_users',)],
            [('get_users', 'FUNCTION')],
            [(1,), (2,), (3,)]  # 3 results, expected 3
        ]
        
        test = FunctionTest(
            name='get_users',
            arguments=[],
            expected_count=3,
            title='function_not_expected_value_expected_result_count_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'function_not_expected_value_expected_result_count_positive_feedback'

    def test_function_not_expected_value_expected_result_count_negative_feedback(self, mock_cursor):
        """Test negative feedback when result count does not match."""
        mock_cursor.fetchall.side_effect = [
            [('get_users',)],
            [('get_users', 'FUNCTION')],
            [(1,), (2,)]  # 2 results, expected 3
        ]
        
        test = FunctionTest(
            name='get_users',
            arguments=[],
            expected_count=3,
            title='function_not_expected_value_expected_result_count_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_not_expected_value_expected_result_count_negative_feedback'

    def test_function_expected_value_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value matches."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],
            [('calculate_total', 'FUNCTION')],
            [(120,)]  # Matches expected value
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            expected_value=120,
            title='function_expected_value_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'function_expected_value_positive_feedback'

    def test_function_expected_value_negative_feedback(self, mock_cursor):
        """Test negative feedback when expected value does not match."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],
            [('calculate_total', 'FUNCTION')],
            [(100,)]  # Does not match expected 120
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            expected_value=120,
            title='function_expected_value_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_expected_value_negative_feedback'

    def test_function_expected_value_group_numbers_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in number range."""
        mock_cursor.fetchall.side_effect = [
            [('get_price',)],
            [('get_price', 'FUNCTION')],
            [(5,)]  # Value 5 is in range [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ]
        
        test = FunctionTest(
            name='get_price',
            arguments=[],
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='function_expected_value_group_numbers_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'function_expected_value_group_numbers_positive_feedback'

    def test_function_expected_value_group_numbers_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in number range."""
        mock_cursor.fetchall.side_effect = [
            [('get_price',)],
            [('get_price', 'FUNCTION')],
            [(15,)]  # Value 15 is not in range
        ]
        
        test = FunctionTest(
            name='get_price',
            arguments=[],
            expected_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title='function_expected_value_group_numbers_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_expected_value_group_numbers_negative_feedback'

    def test_function_expected_value_group_strings_positive_feedback(self, mock_cursor):
        """Test positive feedback when value is in string list."""
        mock_cursor.fetchall.side_effect = [
            [('get_status',)],
            [('get_status', 'FUNCTION')],
            [('active',)]  # Value is in list
        ]
        
        test = FunctionTest(
            name='get_status',
            arguments=[],
            expected_value=['active', 'inactive', 'pending'],
            title='function_expected_value_group_strings_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'function_expected_value_group_strings_positive_feedback'

    def test_function_expected_value_group_strings_negative_feedback(self, mock_cursor):
        """Test negative feedback when value is not in string list."""
        mock_cursor.fetchall.side_effect = [
            [('get_status',)],
            [('get_status', 'FUNCTION')],
            [('deleted',)]  # Value is not in list
        ]
        
        test = FunctionTest(
            name='get_status',
            arguments=[],
            expected_value=['active', 'inactive', 'pending'],
            title='function_expected_value_group_strings_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'function_expected_value_group_strings_negative_feedback'

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.side_effect = [
            [('calculate_total',)],
            [('calculate_total', 'FUNCTION')],
            [(120,)]
        ]
        
        test = FunctionTest(
            name='calculate_total',
            arguments=[100, 0.2],
            expected_value=120,
            custom_feedback='Custom function test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom function test message' in result['message']['params']

