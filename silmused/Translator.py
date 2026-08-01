import json
import glob
import os
from datetime import datetime
from string import Template

supported_format = ['json']

class Translator():
    def __init__(self, locale='et', file_format='json'):
        # initialization
        self.data = {}
        self.locale = locale

        current_file_path = os.path.abspath(__file__)
        root_directory = os.path.dirname(current_file_path)
        locale_directory = os.path.join(root_directory, 'locale')
        # check if format is supported
        if file_format in supported_format:
            # get list of files with specific extensions
            files = glob.glob(f'{locale_directory}/'+f'*.{file_format}')
            for fil in files:
                # get the name of the file without extension, will be used as locale name
                loc = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, 'r', encoding='utf8') as f:
                    if file_format == 'json':
                        self.data[loc] = json.load(f)
        # print(self.data['et'])

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print('Invalid locale')

    def translate(self, test_type, test_key, **kwargs):
        if self.locale not in self.data:
            return "Locale not supported: " + self.locale
        if test_type not in self.data[self.locale]:
            return "Test_type not supported: " + test_type + " FOR locale: " + self.locale
        if test_key not in self.data[self.locale][test_type]:
            return "Test_key not supported: " + test_key + " FOR test_type: " + test_type

        dynamic_kwargs = {
            f"param{index + 1}": (
                param if not isinstance(param, list)
                else self._translate_param_separation(param)
            )
            for index, param in enumerate(kwargs)
        }

        # print(self.data[self.locale][test_type])
        text = self.data[self.locale][test_type].get(test_key, test_key)

        return Template(text).safe_substitute(dynamic_kwargs)

    def _get_lang_param_separator(self, test_type, test_key):
        text = self.data[self.locale][test_type].get(test_key, test_key)
        return text

    def _translate_param_separation(self, param_list):
        or_lang = self._get_lang_param_separator("custom", "or")
        output = ''
        for (index, param) in enumerate(param_list):
            operator = '' if index == 0 else f"' {or_lang} '"
            output += f"{operator}{param}"
        return output


def str_to_datetime(dt_str, format='%Y-%m-%d'):
    return datetime.strptime(dt_str, format)


# def datetime_to_str(dt, format='MMMM dd, yyyy', loc='en'):
#    return format_datetime(dt, format=format, locale=loc)
