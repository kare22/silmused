import json
import glob
import os
from datetime import datetime
from string import Template
supported_format = ['json']

class Translator():
    def __init__(self, locale='et', translations_folder='silmused\\locale', file_format='json'):
        # initialization
        self.data = {}
        self.locale = locale

        # check if format is supported
        if file_format in supported_format:
            # get list of files with specific extensions
            files = glob.glob(f'{translations_folder}/'+f'*.{file_format}')
            #print(glob.glob(f'{translations_folder}/'+f'*.{file_format}'))
            #print(glob.glob('*'))
            for fil in files:
                # get the name of the file without extension, will be used as locale name
                loc = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, 'r', encoding='utf8') as f:
                    if file_format == 'json':
                        self.data[loc] = json.load(f)
        #print(self.data['et'])
    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print('Invalid locale')

    def get_locale(self):
        return self.locale

    def translate(self, test_type, test_key, **kwargs):
        # return the key instead of translation text if locale is not supported
        if self.locale not in self.data:
            return "Locale not supported: " + self.locale + "\n " + str(self.data)
        if test_type not in self.data[self.locale]:
            return "Test_type not supported: " + test_type
        if test_key not in self.data[self.locale][test_type]:
            return "Test_key not supported: " + test_key
        #print(self.data[self.locale][test_type][test_key])
        text = self.data[self.locale][test_type].get(test_key, test_key)

        # string interpolation
        return Template(text).safe_substitute(**kwargs)


def str_to_datetime(dt_str, format='%Y-%m-%d'):
    return datetime.strptime(dt_str, format)


# def datetime_to_str(dt, format='MMMM dd, yyyy', loc='en'):
#    return format_datetime(dt, format=format, locale=loc)
