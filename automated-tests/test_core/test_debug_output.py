from unittest.mock import Mock

from silmused.ExecuteLayer import ExecuteLayer
from silmused.tests.DataTest import DataTest
from silmused.tests.TestDefinition import TestDefinition as _TestDefinition


class FailingDebugTest(_TestDefinition):
    """Concrete test that raises an exception for debug output tests."""

    def execute(self, cursor):
        raise Exception("debug failure")


class TestDebugOutput:
    """Tests for debug levels shared by test classes."""

    def test_debug_level_is_normalized_to_uppercase(self):
        test = DataTest(
            name='users',
            column_name='name',
            debug='debug',
            points=10,
        )

        assert test.debug == 'DEBUG'

    def test_debug_level_outputs_query_result_and_feedback(self, capsys):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('Alice',)]
        test = DataTest(
            name='users',
            column_name='name',
            expected_value='Alice',
            title='debug data test',
            debug='DEBUG',
            points=10,
        )

        result = test.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['is_success'] is True
        assert 'DATA TEST DEBUG:' in captured.out
        assert 'Test title: debug data test' in captured.out
        assert 'query:' in captured.out
        assert "result: [('Alice',)]" in captured.out
        assert 'FEEDBACK DEBUG:' in captured.out
        assert 'Feedback:' in captured.out

    def test_all_debug_level_outputs_extended_fields(self, capsys):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(5,)]
        test = DataTest(
            name='products',
            column_name='price',
            expected_value=[1, 10],
            title='all debug data test',
            debug='ALL',
            points=10,
        )

        result = test.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['is_success'] is True
        assert 'DATA TEST DEBUG:' in captured.out
        assert 'name: products' in captured.out
        assert 'column_name: price' in captured.out
        assert 'expected_value: [1, 10]' in captured.out
        assert 'points: 10' in captured.out
        assert 'test_type: data_test' in captured.out
        assert 'FEEDBACK DEBUG:' in captured.out
        assert 'is_success: True' in captured.out

    def test_invalid_debug_level_outputs_warning(self, capsys):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('Alice',)]
        test = DataTest(
            name='users',
            column_name='name',
            expected_value='Alice',
            debug='verbose',
            points=10,
        )

        result = test.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['is_success'] is True
        assert "Warning! VERBOSE is not valid debug level, choose 'DEBUG' or 'ALL'" in captured.out

    def test_system_error_debug_outputs_exception_and_query(self, capsys):
        mock_cursor = Mock()
        test = FailingDebugTest(
            name='broken',
            points=10,
            query='SELECT broken',
            debug='DEBUG',
        )

        result = test.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['is_success'] is False
        assert 'SYS ERROR DEBUG:' in captured.out
        assert 'ERROR QUERY:' in captured.out
        assert 'SELECT broken' in captured.out
        assert 'FEEDBACK DEBUG:' in captured.out

    def test_execute_layer_debug_outputs_query(self, capsys):
        mock_cursor = Mock()
        layer = ExecuteLayer(query='SELECT 1', debug='DEBUG')

        result = layer.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['message'] == 'Success'
        assert 'query: SELECT 1' in captured.out

    def test_execute_layer_debug_outputs_system_error(self, capsys):
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = [Exception('debug failure'), None]
        layer = ExecuteLayer(query='INVALID SQL', debug='DEBUG')

        result = layer.run(mock_cursor)
        captured = capsys.readouterr()

        assert result['message'] == 'Failure'
        assert 'sys_error:' in captured.out
        assert 'debug failure' in captured.out
