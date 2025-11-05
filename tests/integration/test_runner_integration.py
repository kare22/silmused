"""
Integration tests for Runner class with mocked database operations.
These tests verify that Runner orchestrates components correctly.
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, MagicMock, patch, mock_open
from silmused import Runner
from silmused.tests.StructureTest import StructureTest
from silmused.tests.DataTest import DataTest
from silmused.ChecksLayer import ChecksLayer
from silmused.TitleLayer import TitleLayer
from silmused.ExecuteLayer import ExecuteLayer


class TestRunnerIntegration:
    """Integration tests for Runner class."""

    @patch('silmused.Runner.subprocess.run')
    @patch('silmused.Runner.psycopg2.connect')
    def test_runner_database_test_with_structure_test(self, mock_connect, mock_subprocess):
        """Test Runner with StructureTest on a mock database."""
        # Setup mocks
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        # Mock database query result
        mock_cursor.fetchall.return_value = [('users', 'id', 'integer', None, None, None, None, 'integer', None)]
        
        # Create test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write('INSERT INTO users (id) VALUES (1);')
            test_file = f.name
        
        try:
            # Create tests
            tests = [
                StructureTest(
                    name='users',
                    column_name='id',
                    expected_type='integer',
                    title='Users table has id column',
                    points=10
                )
            ]
            
            # Mock file validation
            with patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=True), \
                 patch('silmused.Runner.Runner._create_db_from_psql_insert'):
                runner = Runner(
                    backup_file_path=test_file,
                    tests=tests,
                    lang='en'
                )
                
                # Verify results structure
                results_json = runner.get_results()
                results = json.loads(results_json)
                
                assert results['result_type'] == 'OK_V3'
                assert 'points' in results
                assert 'tests' in results
                assert len(results['tests']) > 0
        finally:
            os.unlink(test_file)

    @patch('silmused.Runner.subprocess.run')
    @patch('silmused.Runner.psycopg2.connect')
    def test_runner_with_checks_layer(self, mock_connect, mock_subprocess):
        """Test Runner with ChecksLayer containing multiple tests."""
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [('users', 'id', 'integer', None, None, None, None, 'integer', None)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write('INSERT INTO users (id, name) VALUES (1, \'test\');')
            test_file = f.name
        
        try:
            tests = [
                TitleLayer('Database Structure Tests'),
                ChecksLayer(
                    title='Users table validation',
                    tests=[
                        StructureTest(name='users', title='Table exists', points=10),
                        StructureTest(name='users', column_name='id', title='ID column exists', points=10)
                    ]
                )
            ]
            
            with patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=True), \
                 patch('silmused.Runner.Runner._create_db_from_psql_insert'):
                runner = Runner(
                    backup_file_path=test_file,
                    tests=tests,
                    lang='en'
                )
                
                results_json = runner.get_results()
                results = json.loads(results_json)
                
                assert results['result_type'] == 'OK_V3'
                # Should have title layer and checks layer
                assert len(results['tests']) >= 2
        finally:
            os.unlink(test_file)

    @patch('silmused.Runner.subprocess.run')
    @patch('silmused.Runner.psycopg2.connect')
    def test_runner_with_execute_layer(self, mock_connect, mock_subprocess):
        """Test Runner with ExecuteLayer for pre-test queries."""
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [('users', 'id', 'integer', None, None, None, None, 'integer', None)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write('CREATE TABLE users (id INTEGER);')
            test_file = f.name
        
        try:
            tests = [
                ExecuteLayer(query='INSERT INTO users (id) VALUES (1);'),
                StructureTest(name='users', title='Table exists after insert', points=10)
            ]
            
            with patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=True), \
                 patch('silmused.Runner.Runner._create_db_from_psql_insert'):
                runner = Runner(
                    backup_file_path=test_file,
                    tests=tests,
                    lang='en'
                )
                
                # Verify ExecuteLayer was called
                assert mock_cursor.execute.called
                
                results_json = runner.get_results()
                results = json.loads(results_json)
                
                assert results['result_type'] == 'OK_V3'
        finally:
            os.unlink(test_file)

    @patch('silmused.Runner.subprocess.run')
    @patch('silmused.Runner.psycopg2.connect')
    def test_runner_query_test_mode(self, mock_connect, mock_subprocess):
        """Test Runner in query test mode."""
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [('test_value',)]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write('CREATE TABLE songs (title TEXT);')
            test_file = f.name
        
        try:
            from silmused.tests.QueryDataTest import QueryDataTest
            
            tests = [
                QueryDataTest(
                    name='query_test',
                    column_name='title',
                    expected_value='test_value',
                    title='Query returns expected value',
                    points=20
                )
            ]
            
            with patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=True), \
                 patch('silmused.Runner.Runner._create_db_from_psql_insert'), \
                 patch('silmused.Runner.Runner._create_query_view'):
                runner = Runner(
                    backup_file_path=test_file,
                    tests=tests,
                    test_query='query',
                    query_sql='SELECT title FROM songs',
                    lang='en'
                )
                
                results_json = runner.get_results()
                results = json.loads(results_json)
                
                assert results['result_type'] == 'OK_V3'
        finally:
            os.unlink(test_file)

    def test_runner_invalid_file_handling(self):
        """Test Runner handles invalid file gracefully."""
        with patch('silmused.Runner.Runner._file_is_valid_pg_dump', return_value=False), \
             patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=False):
            runner = Runner(
                backup_file_path='nonexistent.sql',
                tests=[],
                lang='en'
            )
            
            # Should not raise exception, but results should be empty or error state
            assert runner.results == []

    def test_runner_empty_query_sql(self):
        """Test Runner handles empty query SQL in query mode."""
        with patch('silmused.Runner.Runner._file_is_valid_pg_dump', return_value=False), \
             patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=False):
            runner = Runner(
                backup_file_path='test.sql',
                tests=[],
                test_query='query',
                query_sql='',
                lang='en'
            )
            
            # Should handle empty query gracefully
            assert runner.results == []

