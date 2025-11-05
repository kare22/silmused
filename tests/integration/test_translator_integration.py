"""
Integration tests for Translator with actual locale files.
"""
import pytest
from silmused.Translator import Translator


class TestTranslatorIntegration:
    """Integration tests for Translator with real locale files."""

    def test_translator_loads_all_locale_files(self):
        """Test that Translator loads all available locale files."""
        translator = Translator()
        
        # Should load at least English and Estonian
        assert 'en' in translator.data
        assert 'et' in translator.data
        assert len(translator.data) >= 2

    def test_translator_complete_translation_workflow(self):
        """Test complete translation workflow with real messages."""
        translator = Translator(locale='en')
        
        # Test structure test messages
        positive = translator.translate(
            'structure_test',
            'table_should_exist_positive_feedback',
            param1='users'
        )
        negative = translator.translate(
            'structure_test',
            'table_should_exist_negative_feedback',
            param1='users'
        )
        
        assert 'users' in positive
        assert 'users' in negative
        assert 'Correct' in positive or 'Correct' in positive.lower()
        assert 'Wrong' in negative or 'Wrong' in negative.lower()

    def test_translator_estonian_locale(self):
        """Test Estonian locale translations."""
        translator = Translator(locale='et')
        
        result = translator.translate(
            'structure_test',
            'table_should_exist_positive_feedback',
            param1='kasutajad'
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'kasutajad' in result

    def test_translator_switch_locale(self):
        """Test switching locales dynamically."""
        translator = Translator(locale='en')
        en_result = translator.translate(
            'structure_test',
            'table_should_exist_positive_feedback',
            param1='test'
        )
        
        translator.set_locale('et')
        et_result = translator.translate(
            'structure_test',
            'table_should_exist_positive_feedback',
            param1='test'
        )
        
        assert en_result != et_result  # Should be different translations
        assert 'test' in en_result
        assert 'test' in et_result

    def test_translator_all_test_types(self):
        """Test that all test types have translations."""
        translator = Translator(locale='en')
        
        test_types = [
            'structure_test',
            'data_test',
            'constraint_test',
            'function_test',
            'procedure_test',
            'query_data_test',
            'query_structure_test',
            'trigger_test',
            'view_test',
            'index_test',
            'sys_fail'
        ]
        
        for test_type in test_types:
            assert test_type in translator.data['en'], f"{test_type} not found in English locale"

