"""
Pytest configuration for integration tests.
"""
import pytest


@pytest.fixture(scope="session")
def mock_postgres_connection():
    """Fixture providing a mock PostgreSQL connection."""
    from unittest.mock import MagicMock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture(scope="function")
def temp_sql_file(tmp_path):
    """Fixture providing a temporary SQL file."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
        yield f.name
    
    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)

