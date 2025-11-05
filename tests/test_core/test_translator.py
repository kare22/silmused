import pytest
from silmused.Translator import Translator


class TestTranslator:
    """Tests for the Translator class."""

    def test_translator_initialization_default_locale(self):
        """Test initialization with default locale (et)."""
        translator = Translator()
        assert translator.locale == 'et'
        assert 'et' in translator.data
        assert 'en' in translator.data

    def test_translator_initialization_custom_locale(self):
        """Test initialization with custom locale."""
        translator = Translator(locale='en')
        assert translator.locale == 'en'

    def test_translator_initialization_loads_locale_files(self):
        """Test that locale files are loaded."""
        translator = Translator()
        assert isinstance(translator.data, dict)
        assert len(translator.data) > 0

    def test_translate_basic_no_parameters(self):
        """Test basic translation without parameters."""
        translator = Translator(locale='en')
        result = translator.translate('structure_test', 'table_should_exist_positive_feedback')
        assert 'Correct' in result
        assert 'table' in result.lower()

    def test_translate_with_one_parameter(self):
        """Test translation with one parameter."""
        translator = Translator(locale='en')
        result = translator.translate('structure_test', 'table_should_exist_positive_feedback', param1='users')
        assert 'users' in result

    def test_translate_with_two_parameters(self):
        """Test translation with two parameters."""
        translator = Translator(locale='en')
        result = translator.translate(
            'structure_test',
            'column_should_exist_positive_feedback',
            param1='email',
            param2='users'
        )
        assert 'email' in result
        assert 'users' in result

    def test_translate_with_three_parameters(self):
        """Test translation with three parameters."""
        translator = Translator(locale='en')
        result = translator.translate(
            'structure_test',
            'expected_character_maximum_length_type_check_positive_feedback',
            param1='255',
            param2='users',
            param3='email'
        )
        assert '255' in result
        assert 'users' in result
        assert 'email' in result

    def test_translate_with_four_parameters(self):
        """Test translation with four parameters."""
        translator = Translator(locale='en')
        result = translator.translate(
            'structure_test',
            'expected_character_maximum_length_type_check_negative_feedback',
            param1='255',
            param2='100',
            param3='users',
            param4='email'
        )
        assert '255' in result
        assert '100' in result
        assert 'users' in result
        assert 'email' in result

    def test_translate_with_five_parameters(self):
        """Test translation with five parameters."""
        translator = Translator(locale='en')
        result = translator.translate(
            'query_data_test',
            'query_expected_value_group_numbers_positive_feedback',
            param1='10',
            param2='5',
            param3='15',
            param4='price',
            param5='products'
        )
        assert '10' in result
        assert '5' in result
        assert '15' in result

    def test_translate_missing_test_type(self):
        """Test translation with missing test_type."""
        translator = Translator(locale='en')
        result = translator.translate('nonexistent_type', 'some_key')
        assert 'Test_type not supported' in result
        assert 'nonexistent_type' in result

    def test_translate_missing_test_key(self):
        """Test translation with missing test_key."""
        translator = Translator(locale='en')
        result = translator.translate('structure_test', 'nonexistent_key')
        assert 'Test_key not supported' in result
        assert 'nonexistent_key' in result

    def test_translate_unsupported_locale(self):
        """Test translation with unsupported locale."""
        translator = Translator(locale='fr')
        result = translator.translate('structure_test', 'table_should_exist_positive_feedback')
        assert 'Locale not supported' in result
        assert 'fr' in result

    def test_set_locale_valid(self):
        """Test set_locale with valid locale."""
        translator = Translator(locale='en')
        translator.set_locale('et')
        assert translator.locale == 'et'

    def test_set_locale_invalid(self):
        """Test set_locale with invalid locale."""
        translator = Translator(locale='en')
        original_locale = translator.locale
        translator.set_locale('invalid_locale')
        # Should not change locale
        assert translator.locale == original_locale

    def test_translate_template_substitution(self):
        """Test that template substitution works correctly."""
        translator = Translator(locale='en')
        result = translator.translate('sys_fail', 'undefined_column', param1='test_column')
        assert 'test_column' in result
        assert 'Cannot be tested' in result

    def test_translate_custom_feedback(self):
        """Test translation with custom_feedback key."""
        translator = Translator(locale='en')
        result = translator.translate('structure_test', 'custom_feedback', param1='Custom message here')
        assert 'Custom message here' in result

    def test_translate_estonian_locale(self):
        """Test translation with Estonian locale."""
        translator = Translator(locale='et')
        result = translator.translate('structure_test', 'table_should_exist_positive_feedback', param1='kasutajad')
        assert isinstance(result, str)
        assert len(result) > 0

