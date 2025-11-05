import pytest
from unittest.mock import Mock, MagicMock
from silmused.ChecksLayer import ChecksLayer
from silmused.tests.TestDefinition import TestDefinition


class MockTest(TestDefinition):
    """Mock test class for testing ChecksLayer."""
    
    def __init__(self, name='test', points=10, should_succeed=True):
        self.should_succeed = should_succeed
        super().__init__(name=name, points=points)
    
    def execute(self, cursor):
        return self.response(self.should_succeed)


class TestChecksLayer:
    """Tests for the ChecksLayer class."""

    def test_checks_layer_initialization_with_title(self):
        """Test initialization with custom title."""
        layer = ChecksLayer(title='Test Group', tests=[])
        assert layer.title == 'Test Group'
        assert layer.tests == []

    def test_checks_layer_initialization_default_title(self):
        """Test initialization with default UUID title."""
        layer = ChecksLayer(tests=[])
        assert layer.title.startswith('test_')
        assert len(layer.title) > 10  # UUID is longer than 'test_'

    def test_checks_layer_initialization_with_tests(self):
        """Test initialization with test list."""
        test1 = MockTest(name='test1', points=10)
        test2 = MockTest(name='test2', points=20)
        layer = ChecksLayer(title='Test Group', tests=[test1, test2])
        assert len(layer.tests) == 2
        assert layer.tests[0] == test1
        assert layer.tests[1] == test2

    def test_checks_layer_run_executes_all_tests(self):
        """Test that run method executes all tests in the layer."""
        mock_cursor = Mock()
        test1 = MockTest(name='test1', points=10, should_succeed=True)
        test2 = MockTest(name='test2', points=20, should_succeed=False)
        layer = ChecksLayer(title='Test Group', tests=[test1, test2])
        
        result = layer.run(mock_cursor)
        
        assert result['title'] == 'Test Group'
        assert result['type'] == 'checks_layer'
        assert 'checks' in result
        assert len(result['checks']) == 2

    def test_checks_layer_run_result_structure(self):
        """Test that run returns correct structure."""
        mock_cursor = Mock()
        test = MockTest(name='test1', points=10)
        layer = ChecksLayer(title='Test Group', tests=[test])
        
        result = layer.run(mock_cursor)
        
        assert isinstance(result, dict)
        assert 'title' in result
        assert 'type' in result
        assert 'checks' in result
        assert result['type'] == 'checks_layer'

    def test_checks_layer_run_empty_tests(self):
        """Test run with empty test list."""
        mock_cursor = Mock()
        layer = ChecksLayer(title='Test Group', tests=[])
        
        result = layer.run(mock_cursor)
        
        assert result['title'] == 'Test Group'
        assert result['checks'] == []

