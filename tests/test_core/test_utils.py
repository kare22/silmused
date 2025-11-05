import pytest
from silmused.utils import list_to_string


class TestListToString:
    """Tests for the list_to_string utility function."""

    def test_list_to_string_none_input(self):
        """Test that None input returns empty string."""
        result = list_to_string(None)
        assert result == ''

    def test_list_to_string_empty_list(self):
        """Test that empty list returns empty string."""
        result = list_to_string([])
        assert result == ''

    def test_list_to_string_strings(self):
        """Test list of strings formatting."""
        result = list_to_string(['apple', 'banana', 'cherry'])
        assert result == "'apple', 'banana', 'cherry'"

    def test_list_to_string_numbers(self):
        """Test list of numbers formatting."""
        result = list_to_string([1, 2, 3])
        assert result == "1, 2, 3"

    def test_list_to_string_mixed_types(self):
        """Test list with mixed types (strings and numbers)."""
        result = list_to_string(['apple', 1, 'banana', 2.5])
        assert result == "'apple', 1, 'banana', 2.5"

    def test_list_to_string_single_item(self):
        """Test list with single item."""
        result = list_to_string(['single'])
        assert result == "'single'"

    def test_list_to_string_single_number(self):
        """Test list with single number."""
        result = list_to_string([42])
        assert result == "42"

    def test_list_to_string_float_numbers(self):
        """Test list with float numbers."""
        result = list_to_string([1.5, 2.7, 3.14])
        assert result == "1.5, 2.7, 3.14"

    def test_list_to_string_strings_with_special_chars(self):
        """Test list of strings with special characters."""
        result = list_to_string(["test'quote", "test\"quote"])
        assert result == "'test'quote', 'test\"quote'"

