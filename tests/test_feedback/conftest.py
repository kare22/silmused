"""
Pytest configuration and fixtures for feedback tests.
"""
import pytest
from unittest.mock import MagicMock, Mock


@pytest.fixture
def mock_cursor():
    """Fixture providing a mock database cursor."""
    cursor = MagicMock()
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Fixture providing a mock database connection."""
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection


@pytest.fixture
def sample_table_result():
    """Sample result for information_schema.columns query (table structure)."""
    return [
        ('users', 'id', 'integer', None, None, None, None, 'integer', None),
        ('users', 'name', 'character varying', 255, None, None, None, 'varchar', 255),
    ]


@pytest.fixture
def sample_constraint_result():
    """Sample result for constraint queries."""
    return [
        ('users', 'id', 'pk_users', 'PRIMARY KEY'),
        ('users', 'email', 'uq_users_email', 'UNIQUE'),
    ]


@pytest.fixture
def sample_function_result():
    """Sample result for function queries."""
    return [
        ('calculate_total', 'FUNCTION', 2),
    ]


@pytest.fixture
def sample_view_result():
    """Sample result for view queries."""
    return [
        ('user_view', 'VIEW'),
    ]


@pytest.fixture
def sample_index_result():
    """Sample result for index queries."""
    return [
        ('idx_users_email',),
    ]


@pytest.fixture
def sample_trigger_result():
    """Sample result for trigger queries."""
    return [
        ('trg_users_updated', 'BEFORE UPDATE'),
    ]

