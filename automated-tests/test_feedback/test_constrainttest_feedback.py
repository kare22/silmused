"""
Tests for ConstraintTest feedback messages.
Tests all feedback keys from the constraint_test section of locale files.
"""
import pytest
from unittest.mock import MagicMock
from silmused.tests.ConstraintTest import ConstraintTest


class TestConstraintTestFeedback:
    """Tests for ConstraintTest feedback generation."""

    def test_table_constraint_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when table has constraints."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            title='table_constraint_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_type'] == 'constraint_test'
        assert result['message']['test_key'] == 'table_constraint_should_exist_positive_feedback'
        assert 'users' in result['message']['params']

    def test_table_constraint_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when table has no constraints."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            title='table_constraint_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_constraint_should_exist_negative_feedback'

    def test_table_column_constraint_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column has constraints."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            title='table_column_constraint_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_should_exist_positive_feedback'
        assert 'users' in result['message']['params']
        assert 'id' in result['message']['params']

    def test_table_column_constraint_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column has no constraints."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            title='table_column_constraint_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_should_exist_negative_feedback'

    def test_table_constraint_name_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when constraint name exists."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            constraint_name='pk_users',
            title='table_constraint_name_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_constraint_name_should_exist_positive_feedback'

    def test_table_constraint_name_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when constraint name does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            constraint_name='nonexistent_constraint',
            title='table_constraint_name_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_constraint_name_should_exist_negative_feedback'

    def test_table_constraint_type_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when constraint type exists."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            constraint_type='PRIMARY KEY',
            title='table_constraint_type_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_constraint_type_should_exist_positive_feedback'

    def test_table_constraint_type_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when constraint type does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            constraint_type='UNIQUE',
            title='table_constraint_type_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_constraint_type_should_exist_negative_feedback'

    def test_table_constraint_name_and_type_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when constraint name and type exist."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            constraint_name='pk_users',
            constraint_type='PRIMARY KEY',
            title='table_constraint_name_and_type_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_constraint_name_and_type_should_exist_positive_feedback'

    def test_table_constraint_name_and_type_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when constraint name and type do not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            constraint_name='pk_users',
            constraint_type='PRIMARY KEY',
            title='table_constraint_name_and_type_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_constraint_name_and_type_should_exist_negative_feedback'

    def test_table_column_constraint_name_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint name exists."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='pk_users',
            title='table_column_constraint_name_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_name_should_exist_positive_feedback'

    def test_table_column_constraint_name_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint name does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='nonexistent',
            title='table_column_constraint_name_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_name_should_exist_negative_feedback'

    def test_table_column_constraint_type_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint type exists."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_type='PRIMARY KEY',
            title='table_column_constraint_type_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_type_should_exist_positive_feedback'

    def test_table_column_constraint_type_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint type does not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_type='UNIQUE',
            title='table_column_constraint_type_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_type_should_exist_negative_feedback'

    def test_table_column_constraint_name_and_type_should_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint name and type exist."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='pk_users',
            constraint_type='PRIMARY KEY',
            title='table_column_constraint_name_and_type_should_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_name_and_type_should_exist_positive_feedback'

    def test_table_column_constraint_name_and_type_should_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint name and type do not exist."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='pk_users',
            constraint_type='PRIMARY KEY',
            title='table_column_constraint_name_and_type_should_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_name_and_type_should_exist_negative_feedback'

    def test_table_constraint_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when table has no constraints (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            should_exist=False,
            title='table_constraint_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_constraint_should_not_exist_positive_feedback'

    def test_table_constraint_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when table has constraints (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            should_exist=False,
            title='table_constraint_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_constraint_should_not_exist_negative_feedback'

    def test_table_column_constraint_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column has no constraints (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='name',
            should_exist=False,
            title='table_column_constraint_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_should_not_exist_positive_feedback'

    def test_table_column_constraint_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column has constraints (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            should_exist=False,
            title='table_column_constraint_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_should_not_exist_negative_feedback'

    def test_table_column_constraint_name_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint name does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='nonexistent',
            should_exist=False,
            title='table_column_constraint_name_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_name_should_not_exist_positive_feedback'

    def test_table_column_constraint_name_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint name exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='pk_users',
            should_exist=False,
            title='table_column_constraint_name_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_name_should_not_exist_negative_feedback'

    def test_table_column_constraint_type_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint type does not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='name',
            constraint_type='UNIQUE',
            should_exist=False,
            title='table_column_constraint_type_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_type_should_not_exist_positive_feedback'

    def test_table_column_constraint_type_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint type exists (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_type='PRIMARY KEY',
            should_exist=False,
            title='table_column_constraint_type_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_type_should_not_exist_negative_feedback'

    def test_table_column_constraint_name_and_type_should_not_exist_positive_feedback(self, mock_cursor):
        """Test positive feedback when column constraint name and type do not exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = []
        
        test = ConstraintTest(
            name='users',
            column_name='name',
            constraint_name='nonexistent',
            constraint_type='UNIQUE',
            should_exist=False,
            title='table_column_constraint_name_and_type_should_not_exist_positive_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is True
        assert result['message']['test_key'] == 'table_column_constraint_name_and_type_should_not_exist_positive_feedback'

    def test_table_column_constraint_name_and_type_should_not_exist_negative_feedback(self, mock_cursor):
        """Test negative feedback when column constraint name and type exist (should_not_exist)."""
        mock_cursor.fetchall.return_value = [('users', 'id', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            column_name='id',
            constraint_name='pk_users',
            constraint_type='PRIMARY KEY',
            should_exist=False,
            title='table_column_constraint_name_and_type_should_not_exist_negative_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['is_success'] is False
        assert result['message']['test_key'] == 'table_column_constraint_name_and_type_should_not_exist_negative_feedback'

    def test_custom_feedback(self, mock_cursor):
        """Test that custom feedback overrides default feedback."""
        mock_cursor.fetchall.return_value = [('users', 'pk_users', 'PRIMARY KEY')]
        
        test = ConstraintTest(
            name='users',
            custom_feedback='Custom constraint test message',
            title='custom_feedback',
            points=10
        )
        
        result = test.run(mock_cursor)
        assert result['message']['test_key'] == 'custom_feedback'
        assert 'Custom constraint test message' in result['message']['params']

