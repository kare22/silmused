import pytest
from unittest.mock import Mock, MagicMock
from silmused.tests.TestDefinition import TestDefinition


class ConcreteTestDefinition(TestDefinition):
    """Concrete implementation of TestDefinition for testing."""
    
    def execute(self, cursor):
        return self.response(True)


class TestTestDefinition:
    """Tests for the TestDefinition base class."""

    def test_test_definition_initialization_valid(self):
        """Test valid initialization."""
        test = ConcreteTestDefinition(name='test_table', points=10)
        assert test.name == 'test_table'
        assert test.points == 10
        assert test.should_exist is True

    def test_test_definition_initialization_with_float_points(self):
        """Test initialization with float points."""
        test = ConcreteTestDefinition(name='test_table', points=10.5)
        assert test.points == 10.5

    def test_test_definition_initialization_invalid_arguments_type(self):
        """Test that non-list arguments raises Exception."""
        with pytest.raises(Exception, match='Parameter "arguments" must be a list'):
            ConcreteTestDefinition(name='test', points=10, arguments='not a list')

    def test_test_definition_initialization_valid_arguments_list(self):
        """Test that list arguments are accepted."""
        test = ConcreteTestDefinition(name='test', points=10, arguments=['arg1', 'arg2'])
        assert test.arguments == ['arg1', 'arg2']

    def test_test_definition_initialization_invalid_points_type(self):
        """Test that non-numeric points raises Exception."""
        with pytest.raises(Exception, match='Parameter "points" must be either an integer or a float'):
            ConcreteTestDefinition(name='test', points='not a number')

    def test_test_definition_initialization_conflict_expected_value_and_count(self):
        """Test that both expected_value and expected_count cannot be specified."""
        with pytest.raises(Exception, match='Both expected_value and check_count cannot be specified'):
            ConcreteTestDefinition(
                name='test',
                points=10,
                expected_value=100,
                expected_count=5
            )

    def test_test_definition_query_building_with_where(self):
        """Test query building with WHERE clause."""
        test = ConcreteTestDefinition(
            name='test',
            points=10,
            query='SELECT * FROM table',
            where="id = 1"
        )
        assert 'WHERE' in test.query
        assert 'id = 1' in test.query

    def test_test_definition_query_building_with_join(self):
        """Test query building with JOIN clause."""
        test = ConcreteTestDefinition(
            name='test',
            points=10,
            query='SELECT * FROM table1',
            join='table2 ON table1.id = table2.id'
        )
        assert 'JOIN' in test.query
        assert 'table2' in test.query

    def test_test_definition_query_building_with_where_and_join(self):
        """Test query building with both WHERE and JOIN."""
        test = ConcreteTestDefinition(
            name='test',
            points=10,
            query='SELECT * FROM table1',
            join='table2 ON table1.id = table2.id',
            where="table1.status = 'active'"
        )
        assert 'JOIN' in test.query
        assert 'WHERE' in test.query
        assert 'table2' in test.query
        assert "status = 'active'" in test.query

    def test_test_definition_response_success(self):
        """Test response method for success."""
        test = ConcreteTestDefinition(name='test', points=10, title='Test Title')
        result = test.response(True)
        
        assert result['is_success'] is True
        assert result['message'] == 'Correct'
        assert result['points'] == 10
        assert result['title'] == 'Test Title'

    def test_test_definition_response_failure(self):
        """Test response method for failure."""
        test = ConcreteTestDefinition(name='test', points=10)
        result = test.response(False)
        
        assert result['is_success'] is False
        assert result['message'] == 'Wrong'
        assert result['points'] == 10

    def test_test_definition_response_custom_message_success(self):
        """Test response with custom success message."""
        test = ConcreteTestDefinition(name='test', points=10)
        result = test.response(True, message_success='Custom success')
        
        assert result['is_success'] is True
        assert result['message'] == 'Custom success'

    def test_test_definition_response_custom_message_failure(self):
        """Test response with custom failure message."""
        test = ConcreteTestDefinition(name='test', points=10)
        result = test.response(False, message_failure='Custom failure')
        
        assert result['is_success'] is False
        assert result['message'] == 'Custom failure'

    def test_test_definition_response_custom_points(self):
        """Test response with custom points override."""
        test = ConcreteTestDefinition(name='test', points=10)
        result = test.response(True, points=5)
        
        assert result['points'] == 5

    def test_test_definition_response_is_sys_fail(self):
        """Test response with is_sys_fail flag."""
        test = ConcreteTestDefinition(name='test', points=10)
        result = test.response(False, is_sys_fail=True)
        
        assert result['is_sys_fail'] is True

    def test_test_definition_undefined_column_error_feedback(self):
        """Test _undefined_column_error_feedback method."""
        test = ConcreteTestDefinition(name='test', points=10)
        sysfeedback = 'column "missing_column" does not exist'
        
        result = test._undefined_column_error_feedback(sysfeedback)
        
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_column'
        assert 'missing_column' in result['message']['params'][0]

    def test_test_definition_undefined_table_error_feedback(self):
        """Test _undefined_table_error_feedback method."""
        test = ConcreteTestDefinition(name='test', points=10)
        sysfeedback = 'relation "missing_table" does not exist'
        
        result = test._undefined_table_error_feedback(sysfeedback)
        
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_table'
        assert 'missing_table' in result['message']['params'][0]

    def test_test_definition_ambiguous_column_error_feedback(self):
        """Test _ambiguous_column_error_feedback method."""
        test = ConcreteTestDefinition(name='test', points=10)
        sysfeedback = 'column reference "id" is ambiguous'
        
        result = test._ambiguous_column_error_feedback(sysfeedback)
        
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'ambiguous_column'

    def test_test_definition_undefined_function_error_feedback_round(self):
        """Test _undefined_function_error_feedback with round function."""
        test = ConcreteTestDefinition(name='test', points=10)
        sysfeedback = 'function round(column_name, 2) does not exist'
        
        result = test._undefined_function_error_feedback(sysfeedback)
        
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'undefined_function_round'

    def test_test_definition_undefined_function_error_feedback_generic(self):
        """Test _undefined_function_error_feedback with generic function error."""
        test = ConcreteTestDefinition(name='test', points=10)
        sysfeedback = 'function nonexistent_func() does not exist'
        
        result = test._undefined_function_error_feedback(sysfeedback)
        
        assert result['is_success'] is False
        assert result['is_sys_fail'] is True

    def test_test_definition_index_error(self):
        """Test _index_error method."""
        test = ConcreteTestDefinition(name='test', points=10)
        
        result = test._index_error()
        
        assert result['is_success'] is False
        assert result['message']['test_type'] == 'sys_fail'
        assert result['message']['test_key'] == 'index_error'
        assert result['message']['params'] == []

    def test_test_definition_run_calls_execute(self):
        """Test that run method calls execute."""
        test = ConcreteTestDefinition(name='test', points=10)
        mock_cursor = Mock()
        
        result = test.run(mock_cursor)
        
        assert result['is_success'] is True

    def test_test_definition_run_handles_exception(self):
        """Test that run method handles exceptions."""
        class FailingTest(TestDefinition):
            def execute(self, cursor):
                raise Exception("Test error")
        
        test = FailingTest(name='test', points=10)
        mock_cursor = Mock()
        
        result = test.run(mock_cursor)
        
        assert result['is_success'] is False
        assert result['is_sys_fail'] is True
        # Should have attempted rollback
        assert mock_cursor.execute.called

    def test_test_definition_run_handles_undefined_column_exception(self):
        """Test that run handles UndefinedColumn exception."""
        class ColumnErrorTest(TestDefinition):
            def execute(self, cursor):
                error = type('UndefinedColumn', (Exception,), {})()
                raise error
        
        test = ColumnErrorTest(name='test', points=10)
        mock_cursor = Mock()
        
        result = test.run(mock_cursor)
        
        assert result['is_success'] is False
        assert 'undefined_column' in str(result['message'])

    def test_test_definition_initialization_all_parameters(self):
        """Test initialization with all optional parameters."""
        test = ConcreteTestDefinition(
            name='test_table',
            points=20,
            title='Test Title',
            where='id > 0',
            join='other_table ON test_table.id = other_table.id',
            column_name='name',
            should_exist=False,
            description='Test description',
            arguments=['arg1'],
            expected_value=100,
            expected_type='varchar',
            expected_character_maximum_length=255,
            custom_feedback='Custom feedback'
        )
        
        assert test.name == 'test_table'
        assert test.points == 20
        assert test.title == 'Test Title'
        assert test.should_exist is False
        assert test.column_name == 'name'
        assert test.description == 'Test description'
        assert test.arguments == ['arg1']
        assert test.expected_value == 100
        assert test.expected_type == 'varchar'
        assert test.expected_character_maximum_length == 255
        assert test.custom_feedback == 'Custom feedback'

