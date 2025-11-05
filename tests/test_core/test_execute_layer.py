import pytest
from unittest.mock import Mock, MagicMock
from silmused.ExecuteLayer import ExecuteLayer


class TestExecuteLayer:
    """Tests for the ExecuteLayer class."""

    def test_execute_layer_initialization(self):
        """Test initialization with query."""
        query = "SELECT * FROM users"
        layer = ExecuteLayer(query=query)
        assert layer.query == query

    def test_execute_layer_run_successful_query(self):
        """Test successful query execution."""
        mock_cursor = Mock()
        query = "SELECT * FROM users"
        layer = ExecuteLayer(query=query)
        
        result = layer.run(mock_cursor)
        
        mock_cursor.execute.assert_called_once_with(query)
        assert result['type'] == 'execution'
        assert result['message'] == 'Success'
        assert result['query'] == query

    def test_execute_layer_run_failed_query(self):
        """Test failed query execution with rollback."""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("SQL Error")
        query = "SELECT * FROM nonexistent"
        layer = ExecuteLayer(query=query)
        
        result = layer.run(mock_cursor)
        
        # Should call execute twice: once for query, once for rollback
        assert mock_cursor.execute.call_count == 2
        assert result['type'] == 'execution'
        assert result['message'] == 'Failure'
        assert result['query'] == query
        assert 'error' in result

    def test_execute_layer_run_rollback_on_error(self):
        """Test that rollback is called on error."""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = [Exception("SQL Error"), None]  # First fails, rollback succeeds
        query = "INVALID SQL"
        layer = ExecuteLayer(query=query)
        
        result = layer.run(mock_cursor)
        
        # Verify rollback was called
        rollback_calls = [call for call in mock_cursor.execute.call_args_list if 'ROLLBACK' in str(call)]
        assert len(rollback_calls) > 0 or mock_cursor.execute.call_count >= 2

    def test_execute_layer_run_result_structure_success(self):
        """Test result structure for successful execution."""
        mock_cursor = Mock()
        query = "INSERT INTO users VALUES (1, 'test')"
        layer = ExecuteLayer(query=query)
        
        result = layer.run(mock_cursor)
        
        assert isinstance(result, dict)
        assert result['type'] == 'execution'
        assert result['message'] == 'Success'
        assert 'query' in result

    def test_execute_layer_run_result_structure_failure(self):
        """Test result structure for failed execution."""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Error")
        query = "INVALID SQL"
        layer = ExecuteLayer(query=query)
        
        result = layer.run(mock_cursor)
        
        assert isinstance(result, dict)
        assert result['type'] == 'execution'
        assert result['message'] == 'Failure'
        assert 'error' in result
        assert 'query' in result

