import pytest
import json
import os
import tempfile
from unittest.mock import Mock, MagicMock, patch, mock_open
from silmused.Runner import Runner
from silmused.tests.TestDefinition import TestDefinition


class MockTest(TestDefinition):
    """Mock test class for testing Runner."""
    
    def __init__(self, name='test', points=10, should_succeed=True):
        self.should_succeed = should_succeed
        super().__init__(name=name, points=points)
    
    def execute(self, cursor):
        return self.response(self.should_succeed)


class TestRunner:
    """Tests for the Runner class."""

    def test_runner_initialization_database_name_without_test_name(self):
        """Test database name generation without test_name."""
        with patch('silmused.Runner.Runner._file_is_valid_pg_dump', return_value=False), \
             patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=False):
            runner = Runner(backup_file_path='test.sql', tests=[])
            assert runner.db_name.startswith('db_')
            assert 'test' in runner.db_name
            assert runner.db_name.count('_') >= 2

    def test_runner_initialization_database_name_with_test_name(self):
        """Test database name generation with test_name."""
        with patch('silmused.Runner.Runner._file_is_valid_pg_dump', return_value=False), \
             patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=False):
            runner = Runner(backup_file_path='test.sql', tests=[], test_name='mytest')
            assert runner.db_name.startswith('db_mytest_')
            assert 'test' in runner.db_name

    def test_runner_initialization_parameter_storage(self):
        """Test that all parameters are stored correctly."""
        with patch('silmused.Runner.Runner._file_is_valid_pg_dump', return_value=False), \
             patch('silmused.Runner.Runner._file_is_valid_pg_insert', return_value=False):
            runner = Runner(
                backup_file_path='test.sql',
                tests=[],
                lang='et',
                test_name='test',
                db_user='user',
                db_host='host',
                db_password='pass',
                db_port='5433',
                test_query='query',
                query_sql='SELECT * FROM test',
                encoding='UTF-8'
            )
            assert runner.file_path == 'test.sql'
            assert runner.test_name == 'test'
            assert runner.db_user == 'user'
            assert runner.db_host == 'host'
            assert runner.db_password == 'pass'
            assert runner.db_port == '5433'
            assert runner.test_query == 'query'
            assert runner.query_sql == 'SELECT * FROM test'
            assert runner.encoding == 'UTF-8'
            from silmused.Translator import Translator
            assert isinstance(runner.translator, Translator)

    def test_runner_file_is_valid_pg_dump_valid_file(self):
        """Test _file_is_valid_pg_dump with valid PGDMP file."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.dump'
        
        with patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data=b'PGDMP\x01\x02\x03')):
            result = runner._file_is_valid_pg_dump()
            assert result is True

    def test_runner_file_is_valid_pg_dump_invalid_file(self):
        """Test _file_is_valid_pg_dump with invalid file."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.dump'
        
        with patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data=b'INVALID\x01\x02\x03')):
            result = runner._file_is_valid_pg_dump()
            assert result is False

    def test_runner_file_is_valid_pg_dump_nonexistent_file(self):
        """Test _file_is_valid_pg_dump with non-existent file."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'nonexistent.dump'
        
        with patch('os.path.isfile', return_value=False):
            result = runner._file_is_valid_pg_dump()
            assert result is False

    def test_runner_file_is_valid_pg_dump_io_error(self):
        """Test _file_is_valid_pg_dump with IOError."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.dump'
        
        with patch('os.path.isfile', return_value=True), \
             patch('builtins.open', side_effect=IOError()):
            result = runner._file_is_valid_pg_dump()
            assert result is False

    def test_runner_file_is_valid_pg_insert_valid_file(self):
        """Test _file_is_valid_pg_insert with valid SQL file containing INSERT."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.sql'
        runner.encoding = 'UTF-8'
        
        with patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data='INSERT INTO test VALUES (1);')):
            result = runner._file_is_valid_pg_insert()
            assert result is True

    def test_runner_file_is_valid_pg_insert_invalid_extension(self):
        """Test _file_is_valid_pg_insert with invalid extension."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.txt'
        runner.encoding = 'UTF-8'
        
        with patch('os.path.isfile', return_value=True):
            result = runner._file_is_valid_pg_insert()
            assert result is False

    def test_runner_file_is_valid_pg_insert_no_insert(self):
        """Test _file_is_valid_pg_insert with file without INSERT."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'test.sql'
        runner.encoding = 'UTF-8'
        
        with patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data='SELECT * FROM test;')):
            result = runner._file_is_valid_pg_insert()
            assert result is False

    def test_runner_file_is_valid_pg_insert_nonexistent_file(self):
        """Test _file_is_valid_pg_insert with non-existent file."""
        runner = Runner.__new__(Runner)
        runner.file_path = 'nonexistent.sql'
        runner.encoding = 'UTF-8'
        
        with patch('os.path.isfile', return_value=False):
            result = runner._file_is_valid_pg_insert()
            assert result is False

    def test_runner_message_to_feedback_zero_params(self):
        """Test _message_to_feedback with zero parameters."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        runner.translator.translate.return_value = 'Translated message'
        
        message = {
            'test_type': 'structure_test',
            'test_key': 'table_should_exist_positive_feedback',
            'params': []
        }
        
        result = runner._message_to_feedback(message)
        assert result == 'Translated message'
        runner.translator.translate.assert_called_once_with('structure_test', 'table_should_exist_positive_feedback')

    def test_runner_message_to_feedback_one_param(self):
        """Test _message_to_feedback with one parameter."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        runner.translator.translate.return_value = 'Translated message'
        
        message = {
            'test_type': 'structure_test',
            'test_key': 'table_should_exist_positive_feedback',
            'params': ['users']
        }
        
        result = runner._message_to_feedback(message)
        runner.translator.translate.assert_called_once_with(
            'structure_test', 'table_should_exist_positive_feedback', param1='users'
        )

    def test_runner_message_to_feedback_five_params(self):
        """Test _message_to_feedback with five parameters."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        runner.translator.translate.return_value = 'Translated message'
        
        message = {
            'test_type': 'query_data_test',
            'test_key': 'query_expected_value_group_numbers_positive_feedback',
            'params': ['10', '5', '15', 'price', 'products']
        }
        
        result = runner._message_to_feedback(message)
        runner.translator.translate.assert_called_once_with(
            'query_data_test', 'query_expected_value_group_numbers_positive_feedback',
            param1='10', param2='5', param3='15', param4='price', param5='products'
        )

    def test_runner_message_to_feedback_more_than_five_params(self):
        """Test _message_to_feedback with more than five parameters."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        
        message = {
            'test_type': 'test',
            'test_key': 'key',
            'params': ['1', '2', '3', '4', '5', '6']
        }
        
        result = runner._message_to_feedback(message)
        assert result == "Params were given, but there is more than 5"

    def test_runner_checks_to_object_execution_type(self):
        """Test _checks_to_object with execution type (should be skipped)."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        
        checks = [
            {'type': 'execution', 'message': 'Success'}
        ]
        
        points_max, points_actual, outputs, output_pass = runner._checks_to_object(checks)
        assert points_max == 0
        assert points_actual == 0
        assert len(outputs) == 0

    def test_runner_checks_to_object_message_type(self):
        """Test _checks_to_object with message type."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        
        checks = [
            {'type': 'message', 'message': 'Section Title'}
        ]
        
        points_max, points_actual, outputs, output_pass = runner._checks_to_object(checks)
        assert len(outputs) == 1
        assert outputs[0]['title'] == 'Section Title'
        assert outputs[0]['status'] == 'PASS'

    def test_runner_checks_to_object_with_successful_check(self):
        """Test _checks_to_object with successful check."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        
        checks = [
            {
                'type': 'check',
                'title': 'Test check',
                'points': 10,
                'is_success': True
            }
        ]
        
        points_max, points_actual, outputs, output_pass = runner._checks_to_object(checks)
        assert points_max == 10
        assert points_actual == 10
        assert output_pass is True
        assert outputs[0]['status'] == 'PASS'
        assert outputs[0]['title'] == 'Test check'

    def test_runner_checks_to_object_with_failed_check(self):
        """Test _checks_to_object with failed check."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        runner.translator.translate.return_value = 'Error message'
        
        checks = [
            {
                'type': 'check',
                'title': 'Test check',
                'points': 10,
                'is_success': False,
                'is_sys_fail': False,
                'message': {'test_type': 'test', 'test_key': 'key', 'params': []}
            }
        ]
        
        points_max, points_actual, outputs, output_pass = runner._checks_to_object(checks)
        assert points_max == 10
        assert points_actual == 0
        assert output_pass is False
        assert outputs[0]['status'] == 'FAIL'
        assert 'feedback' in outputs[0]

    def test_runner_results_to_object_with_checks_layer(self):
        """Test _results_to_object with checks_layer type."""
        runner = Runner.__new__(Runner)
        runner.translator = Mock()
        runner.translator.translate.return_value = 'Message'
        
        runner.results = [
            {
                'type': 'checks_layer',
                'title': 'Test Group',
                'checks': [
                    {'type': 'check', 'title': 'Check 1', 'points': 10, 'is_success': True}
                ]
            }
        ]
        
        tests, points_max, points_actual = runner._results_to_object()
        assert len(tests) == 1
        assert tests[0]['title'] == 'Test Group'
        assert 'checks' in tests[0]
        assert points_max == 10
        assert points_actual == 10

    def test_runner_results_to_object_with_message_type(self):
        """Test _results_to_object with message type."""
        runner = Runner.__new__(Runner)
        runner.results = [
            {'type': 'message', 'message': 'Section Title'}
        ]
        
        tests, points_max, points_actual = runner._results_to_object()
        assert len(tests) == 1
        assert tests[0]['title'] == 'Section Title'
        assert tests[0]['status'] == 'PASS'

    def test_runner_get_results_basic(self):
        """Test get_results with basic test results."""
        runner = Runner.__new__(Runner)
        runner.results = [
            {
                'type': 'test',
                'title': 'Test 1',
                'points': 20,
                'is_success': True
            },
            {
                'type': 'test',
                'title': 'Test 2',
                'points': 30,
                'is_success': False
            }
        ]
        
        result_json = runner.get_results()
        result = json.loads(result_json)
        
        assert result['result_type'] == 'OK_V3'
        assert result['points'] == 40  # 20/50 * 100 = 40
        assert 'producer' in result
        assert 'finished_at' in result
        assert len(result['tests']) == 2

    def test_runner_get_results_praks_logic(self):
        """Test get_results with praks logic (tests but no points)."""
        runner = Runner.__new__(Runner)
        runner.results = [
            {
                'type': 'message',
                'message': 'Section Title'
            }
        ]
        
        result_json = runner.get_results()
        result = json.loads(result_json)
        
        assert result['points'] == 100  # praks logic: 1/1 * 100 = 100

    def test_runner_get_results_zero_points(self):
        """Test get_results with zero points."""
        runner = Runner.__new__(Runner)
        runner.results = []
        
        result_json = runner.get_results()
        result = json.loads(result_json)
        
        assert result['points'] == 0
        assert result['result_type'] == 'OK_V3'

    def test_runner_get_results_exception_handling(self):
        """Test get_results exception handling."""
        runner = Runner.__new__(Runner)
        runner.results = None  # This will cause an exception in _results_to_object
        
        result_json = runner.get_results()
        result = json.loads(result_json)
        
        assert result['result_type'] == 'OK_V3'
        assert result['points'] == 0
        assert 'producer' in result

