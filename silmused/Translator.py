import json
import glob
import os
from datetime import datetime
from string import Template
supported_format = ['json']
"""data = {"en": {
    "StructureTest": {
        "expected_value_should_exist_positive_feedback": "Correct, expected $correct_value",
        "expected_value_should_exist_negative_feedback": "Wrong, did not expect $wrong_value, expected $correct_value",
        "expected_value_should_not_exist_positive_feedback": "Correct, did not want $correct_value",
        "expected_value_should_not_exist_negative_feedback": "Wrong, this should not exist $wrong_value, expected $correct_value",
        "no_expected_value_table_column_should_exist_positive_feedback": "Correct, column or table $column_name found in table $table_name",
        "no_expected_value_table_column_should_exist_negative_feedback": "Expected to find column or table $column_name, but none were found in $table_name",
        "no_expected_value_table_column_should_not_exist_positive_feedback": "Correct, no column or table named $column_name found in $table_name",
        "no_expected_value_table_column_should_not_exist_negative_feedback": "Expected to not find column or table $column_name in table $table_name"
    },
    "DataTest": {
        "no_expected_value_should_exist_positive_feedback": "Correct, no results found for table $table_name and column(s) $column_name",
        "no_expected_value_should_exist_negative_feedback": "Expected to find no results for table $table_name and column(s) $column_name but none were found",
        "no_expected_value_should_not_exist_positive_feedback": "Correct, no results found for table $table_name and column(s) $column_name",
        "no_expected_value_should_not_exist_negative_feedback": "Expected to find no results for table $table_name and column(s) $column_name but some were found",
        "expected_value_should_exist_positive_feedback": "Correct value found for table $table_name and column(s) $column_name",
        "expected_value_should_exist_negative_feedback": "Expected to find $expected_value for table $table_name and column(s) $column_name but found $wrong_value",
        "expected_value_should_not_exist_positive_feedback": "Correct, $expected_value does not equal $wrong_value in $table_name and column(s) $column_name",
        "expected_value_should_not_exist_negative_feedback": "Expected $expected_value to not equal $wrong_value in table $table_name and column(s) $column_name"
    },
    "ConstraintTest": {
        "constraint_should_exist_positive_feedback": "Correct, $feedback was found",
        "constraint_should_exist_negative_feedback": "Expected to find $feedback but none were found",
        "constraint_should_not_exist_positive_feedback": "Correct, $feedback was not found",
        "constraint_should_not_exist_negative_feedback": "Expected to not find $feedback, but was"
    },
    "IndexTest": {
        "index_positive_feedback": "Correct, index was $index_name found",
        "index_negative_feedback": "Expected to find index $index_name but none were found"
    }
},
    "et": {
        "StructureTest": {
            "expected_value_should_exist_positive_feedback": "Õige, oodatud vastus oli $Õige_value",
            "expected_value_should_exist_negative_feedback": "Vale, ei oodatud vastust $wrong_value, vaid $Õige_value",
            "expected_value_should_not_exist_positive_feedback": "Õige, ei soovitud vastust $Õige_value",
            "expected_value_should_not_exist_negative_feedback": "Vale, ei soovitud vastust $wrong_value, vaid $Õige_value",
            "no_expected_value_table_column_should_exist_positive_feedback": "Õige, tabel või veerg $column_name leitud tabelis $table_name",
            "no_expected_value_table_column_should_exist_negative_feedback": "Vale, tabelit või veergu $column_name, ei leitud tabelis $table_name",
            "no_expected_value_table_column_should_not_exist_positive_feedback": "Õige, tabelit või veergu $column_name ei leitud tabelis $table_name",
            "no_expected_value_table_column_should_not_exist_negative_feedback": "Vale, ei tohiks leida tabelit või veergu $column_name tabelis $table_name"
        },
        "DataTest": {
            "no_expected_value_should_exist_positive_feedback": "Õige, ei leitud tulemusi tabelis $table_name ja veerus $column_name",
            "no_expected_value_should_exist_negative_feedback": "Vale, leiti tulemusi tabelis $table_name ja veerus $column_name, aga ei tohiks leida",
            "no_expected_value_should_not_exist_positive_feedback": "Õige, ei leitud tulemusi tabelis $table_name ja veerus $column_name",
            "no_expected_value_should_not_exist_negative_feedback": "Vale, leiti tulemusi tabelis $table_name ja veerus $column_name, aga ei tohiks leida",
            "expected_value_should_exist_positive_feedback": "Õige, tulemus on leitud tabelis $table_name ja veerus $column_name",
            "expected_value_should_exist_negative_feedback": "Vale oodati leida tulemust $expected_value tabelis $table_name ja veerus $column_name, aga leiti $wrong_value",
            "expected_value_should_not_exist_positive_feedback": "Õige, tulemus $expected_value ei võrdu väärtusega $wrong_value tabelis $table_name ja veerus $column_name",
            "expected_value_should_not_exist_negative_feedback": "Vale, tulemus $Vale_value ei tohi võrduda väärtusega $wrong_value tabelis $table_name ja veerus $column_name"
        },
        "ConstraintTest": {
            "constraint_should_exist_positive_feedback": "Õige, kitsendus $feedback on olemas",
            "constraint_should_exist_negative_feedback": "Vale, kitsendus $feedback ei ole olemas",
            "constraint_should_not_exist_positive_feedback": "Õige, kitsendust $feedback ei leitud",
            "constraint_should_not_exist_negative_feedback": "Vale, kitsendust $feedback ei tohtinud leida, aga leiti"
        },
        "IndexTest": {
            "index_positive_feedback": "Õige, indeks $index_name on olemas",
            "index_negative_feedback": "Vale, indeks $index_name ei ole olemas"
        }
    }
}"""


class Translator():
    def __init__(self, locale='et', translations_folder='locale', file_format='json'):
        # initialization
        self.data = {}
        self.locale = locale

        # check if format is supported
        if file_format in supported_format:
            # get list of files with specific extensions
            files = glob.glob(f'{translations_folder}/'+f'*.{file_format}')
            for fil in files:
                # get the name of the file without extension, will be used as locale name
                loc = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, 'r', encoding='utf8') as f:
                    if file_format == 'json':
                        self.data[loc] = json.load(f)
        #print(data)
    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print('Invalid locale')

    def get_locale(self):
        return self.locale

    def translate(self, test_type, key, **kwargs):
        # return the key instead of translation text if locale is not supported
        if self.locale not in self.data:
            return self.locale
        if test_type not in self.data[self.locale]:
            return test_type

        text = self.data[self.locale][test_type].get(key, key)

        # string interpolation
        return Template(text).safe_substitute(**kwargs)


def str_to_datetime(dt_str, format='%Y-%m-%d'):
    return datetime.strptime(dt_str, format)


# def datetime_to_str(dt, format='MMMM dd, yyyy', loc='en'):
#    return format_datetime(dt, format=format, locale=loc)
"""

        #self.translator = Language.Translator()
#self.translator.translate('StructureTest', 'expected_value_should_exist_positive_feedback',correct_value=self.query),
#self.translator.translate('StructureTest', 'expected_value_should_exist_negative_feedback',wrong_value=self.query)
"""

translator = Translator()
#translator.translate('StructureTest', 'expected_value_should_exist_positive_feedback')