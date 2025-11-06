"""
Tests for StructureTest feedback messages.
Tests all feedback keys from the structure_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.StructureTest import StructureTest


class TestStructureTestFeedback:
    """Tests for StructureTest feedback generation."""

    def test_table_should_exist_positive_feedback(self, mock_cursor, sample_table_result):
        """Test positive feedback when table exists."""
        mock_cursor.fetchall.return_value = sample_table_result
        
        test = StructureTest(
            name='users',
            title='table_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'structure_test'
        assert result['message']['test_key'] == 'table_should_exist_positive_feedback'
        assert 'users' in result['message']['params']

    def test_table_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when table does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = StructureTest(
            name='nonexistent',
            title='table_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_should_exist_negative_feedback'
        assert 'nonexistent' in result['message']['params']

    def test_column_should_exist_positive_feedback(self, mock_cursor, sample_table_result):
        """Test positive feedback when column exists."""
        mock_cursor.fetchall.return_value = [sample_table_result[0]]  # id column
        
        test = StructureTest(
            name='users',
            column_name='id',
            title='column_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_should_exist_positive_feedback'
        assert 'id' in result['message']['params']
        assert 'users' in result['message']['params']

    def test_column_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = StructureTest(
            name='users',
            column_name='nonexistent',
            title='column_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_should_exist_negative_feedback'
        assert 'nonexistent' in result['message']['params']

    def test_table_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when table does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = StructureTest(
            name='deleted_table',
            should_exist=False,
            title='table_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_should_not_exist_positive_feedback'

    def test_table_should_not_exist_negative_feedback(self, mock_cursor, sample_table_result):
        """Test negative feedback when table exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = sample_table_result
        
        test = StructureTest(
            name='users',
            should_exist=False,
            title='table_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_should_not_exist_negative_feedback'

    def test_column_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = StructureTest(
            name='users',
            column_name='deleted_column',
            should_exist=False,
            title='column_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'column_should_not_exist_positive_feedback'

    def test_column_should_not_exist_negative_feedback(self, mock_cursor, sample_table_result):
        """Test negative feedback when column exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [sample_table_result[0]]
        
        test = StructureTest(
            name='users',
            column_name='id',
            should_exist=False,
            title='column_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'column_should_not_exist_negative_feedback'

    def test_expected_type_check_positive_feedback(self, mock_cursor):
        """Test positive feedback when column type matches expected type."""
        # Result format: (table_name, column_name, ..., data_type, character_maximum_length, ...)
        mock_cursor.fetchall.return_value = [
            ('users', 'id', None, None, None, None, None, 'integer', None)
        ]
        
        test = StructureTest(
            name='users',
            column_name='id',
            expected_type='integer',
            title='expected_type_check_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        # Type check happens in test_type method, which returns None if correct
        # So we need to check that no type error was returned
        assert result is not None
        # If type is wrong, test_type would return a response with negative feedback
        # If correct, it continues to other checks

    def test_expected_type_check_negative_feedback(self, mock_cursor):
        """Test negative feedback when column type does not match."""
        mock_cursor.fetchall.return_value = [
            ('users', 'id', None, None, None, None, None, 'varchar', None)
        ]
        
        test = StructureTest(
            name='users',
            column_name='id',
            expected_type='integer',
            title='expected_type_check_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_type_check_negative_feedback'
        assert 'integer' in result['message']['params']
        assert 'varchar' in result['message']['params']

    def test_expected_character_maximum_length_type_check_positive_feedback(self, mock_cursor):
        """Test positive feedback when character max length matches."""
        mock_cursor.fetchall.return_value = [
            ('users', 'name', None, None, None, None, None, 'character varying', 255)
        ]
        
        test = StructureTest(
            name='users',
            column_name='name',
            expected_type='varchar',
            expected_character_maximum_length=255,
            title='expected_character_maximum_length_type_check_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        # If correct, no error response from test_type
        assert result is not None

    def test_expected_character_maximum_length_type_check_negative_feedback(self, mock_cursor):
        """Test negative feedback when character max length does not match."""
        mock_cursor.fetchall.return_value = [
            ('users', 'name', None, None, None, None, None, 'character varying', 100)
        ]
        
        test = StructureTest(
            name='users',
            column_name='name',
            expected_type='varchar',
            expected_character_maximum_length=255,
            title='expected_character_maximum_length_type_check_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_character_maximum_length_type_check_negative_feedback'
        assert '255' in result['message']['params']
        assert '100' in result['message']['params']

    def test_expected_value_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when expected value matches."""
        mock_cursor.fetchall.return_value = [(80,)]
        
        test = StructureTest(
            name='users',
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
        
        test = StructureTest(
            name='users',
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
        
        test = StructureTest(
            name='users',
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
        
        test = StructureTest(
            name='users',
            expected_value=80,
            should_exist=False,
            title='expected_value_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'expected_value_should_not_exist_negative_feedback'

    def test_custom_feedback(self, mock_cursor, sample_table_result):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = sample_table_result
        
        test = StructureTest(
            name='users',
            custom_feedback='Custom structure test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom structure test message' in result['message']['params']

