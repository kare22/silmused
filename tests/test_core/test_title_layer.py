import pytest
from unittest.mock import Mock
from silmused.TitleLayer import TitleLayer


class TestTitleLayer:
    """Tests for the TitleLayer class."""

    def test_title_layer_initialization(self):
        """Test initialization with title."""
        title = "Section Title"
        layer = TitleLayer(title=title)
        assert layer.title == title

    def test_title_layer_run_returns_correct_structure(self):
        """Test that run returns correct structure."""
        title = "Database Structure"
        layer = TitleLayer(title=title)
        mock_cursor = Mock()  # TitleLayer accepts any parameter but doesn't use it
        
        result = layer.run(mock_cursor)
        
        assert isinstance(result, dict)
        assert result['type'] == 'title'
        assert result['message'] == title

    def test_title_layer_run_with_none(self):
        """Test run method with None parameter."""
        title = "Test Section"
        layer = TitleLayer(title=title)
        
        result = layer.run(None)
        
        assert result['type'] == 'title'
        assert result['message'] == title

    def test_title_layer_run_with_different_parameters(self):
        """Test that run method accepts any parameter."""
        title = "Test Section"
        layer = TitleLayer(title=title)
        
        # Should work with any parameter type
        result1 = layer.run("string")
        result2 = layer.run(123)
        result3 = layer.run(["list"])
        
        assert result1['message'] == title
        assert result2['message'] == title
        assert result3['message'] == title

