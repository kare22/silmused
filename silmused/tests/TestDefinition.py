import sys
import re


# TODO this should not be usable without a child
class TestDefinition:
    def __init__(self, name, points, title='', where=None, join=None, column_name=None, should_exist=True, query='',
                 description=None, arguments=None, expected_value=None, expected_character_maximum_length=None,
                 expected_type=None, expected_count=None, pre_query=None, after_query=None):
        if arguments is not None and not isinstance(arguments, list):
            raise Exception('Parameter "arguments" must be a list')

        if expected_count is not None and not isinstance(expected_count, int):
            raise Exception('Parameter "expected_count" must be an integer')

        if not isinstance(points, int) and not isinstance(points, float):
            raise Exception('Parameter "points" must be either an integer or a float')

        if expected_value is not None and expected_count is not None:
            raise Exception('Both expected_value and check_count cannot be specified in a single test')

        query_builder = query

        # TODO right now a single join is possible (without a hack)
        if join is not None:
            query_builder += f" JOIN {join}"

        if where is not None:
            query_builder += f" WHERE ({where})"

        self.title = title
        self.points = points
        self.name = name
        self.column_name = column_name
        self.description = description
        self.arguments = arguments  # TODO arguments could be a class
        self.expected_value = expected_value
        self.expected_character_maximum_length = expected_character_maximum_length
        self.expected_type = expected_type
        self.expected_count = expected_count
        self.query = query_builder
        self.pre_query = pre_query
        self.after_query = after_query
        self.should_exist = should_exist  # TODO should be renamed to something more descriptive (should_be_false/falsy)

    # TODO should be callable only inside the scope
    def execute(self, cursor):
        raise NotImplementedError('Method "execute" not implemented')

    def run(self, cursor):
        try:
            # TODO could executing of pre and/or after queries be handled here?
            # print(self.query)
            return self.execute(cursor)
        except:
            # TODO better handler for rollback?
            print(sys.exc_info())
            cursor.execute('ROLLBACK')
            if 'UndefinedColumn' in str(sys.exc_info()[0]):
                return self._undefined_column_error_feedback(str(sys.exc_info()[1]))
            if 'UndefinedTable' in str(sys.exc_info()[0]):
                return self._undefined_table_error_feedback(str(sys.exc_info()[1]))
            if 'AmbiguousColumn' in str(sys.exc_info()[0]):
                return self._ambiguous_column_error_feedback(str(sys.exc_info()[1]))
            if 'UndefinedFunction' in str(sys.exc_info()[0]):
                return self._undefined_function_error_feedback(str(sys.exc_info()[1]))
            if 'IndexError' in str(sys.exc_info()[0]):
                return self._index_error()
            return self.response(
                False,
                message_failure=sys.exc_info(),
                is_sys_fail=True
            )

    # TODO should be callable only inside the scope
    def response(self, is_success, message_success=None, message_failure=None, points=None, is_sys_fail=None):
        if is_success:
            message_statement = 'Correct' if message_success is None else message_success
        else:
            message_statement = 'Wrong' if message_failure is None else message_failure

        return {
            'is_success': is_success,
            'message': message_statement,
            'points': points if points is not None else self.points,
            'description': self.description,
            'query': self.query,
            'pre_query': self.pre_query,
            'after_query': self.after_query,
            'should_exist': self.should_exist,
            'title': self.title,
            'is_sys_fail': is_sys_fail,
        }

    def _undefined_column_error_feedback(self, sysfeedback):
        split_sys_feedback = sysfeedback.split('"')

        return self.response(
            False,
            '',
            {"test_type": "sys_fail",
             "test_key": "undefined_column",
             "params": [split_sys_feedback[1]]},
        )

    def _undefined_table_error_feedback(self, sysfeedback):
        split_sys_feedback = sysfeedback.split('"')

        return self.response(
            False,
            '',
            {"test_type": "sys_fail",
             "test_key": "undefined_table",
             "params": [split_sys_feedback[1]]},
        )

    def _ambiguous_column_error_feedback(self, sysfeedback):
        split_sys_feedback = sysfeedback.split('"')
        # print(sysfeedback)
        return self.response(
            False,
            '',
            {"test_type": "sys_fail",
             "test_key": "ambiguous_column",
             "params": [split_sys_feedback[1]]},
        )

    def _undefined_function_error_feedback(self, sysfeedback):
        if 'round' in sysfeedback:
            pattern = r'SELECT round\((.*?),[0-9]\)'
            match = re.findall(pattern, sysfeedback, re.IGNORECASE)
            if len(match) > 0:
                return self.response(
                    False,
                    '',
                    {"test_type": "sys_fail",
                     "test_key": "undefined_function_round",
                     "params": [match[0]]},
                )

        return self.response(
                False,
                message_failure=sysfeedback,
                is_sys_fail=True
            )

    def _index_error(self):
        return self.response(
            False,
            '',
            {"test_type": "sys_fail",
             "test_key": "index_error",
             "params": []},
        )
