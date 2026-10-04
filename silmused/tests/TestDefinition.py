import sys
import re


class TestDefinition:
    def __init__(self, name, points, title='', where=None, join=None, column_name=None, should_exist=True, query='',
                 description=None, arguments=None, expected_value=None, expected_character_maximum_length=None,
                 expected_type=None, expected_count=None, pre_query=None, after_query=None, custom_feedback=None,
                 elements=None, column_name_fallback=None, expected_value_query=None, llm_check=None, debug=None):
        if arguments is not None:
            if not isinstance(arguments, list):
                raise Exception('Parameter "arguments" must be a list')
            if len(arguments) == 0:
                raise Exception('Parameter "arguments" cannot be an empty list')

        if not isinstance(points, int) and not isinstance(points, float):
            raise Exception('Parameter "points" must be either an integer or a float')

        if expected_value is not None and expected_count is not None:
            raise Exception('Both expected_value and check_count cannot be specified in a single test')

        self.title = title
        self.points = points
        self.name = name
        self.column_name = column_name
        self.where = where
        self.join = join
        self.description = description
        self.arguments = arguments
        self.expected_value = expected_value
        self.expected_character_maximum_length = expected_character_maximum_length
        self.expected_type = expected_type
        self.expected_count = expected_count
        self.query = self.query_builder(query)
        self.pre_query = pre_query
        self.after_query = after_query
        self.should_exist = should_exist
        self.custom_feedback = custom_feedback
        self.elements = elements
        self.column_name_fallback = column_name_fallback
        self.expected_value_query = expected_value_query
        self.llm_check = llm_check
        self.debug = debug.upper() if debug is not None else debug

    def query_builder(self, query):
        query_builder = query
        # right now a single join is possible (without a hack)
        if self.join is not None:
            query_builder += f" JOIN {self.join}"

        if self.where is not None:
            query_builder += f" WHERE ({self.where})"
        return query_builder

    def execute(self, cursor):
        raise NotImplementedError('Method "execute" not implemented')

    def run(self, cursor):
        if self.llm_check:
            cursor.execute(self.query)
            self._llm_check(cursor.fetchall())
        try:
            # could executing of pre and/or after queries be handled here?
            return self.execute(cursor)
        except:
            cursor.execute('ROLLBACK')
            if self.debug is not None:
                if self.debug == 'DEBUG' or self.debug == 'ALL':
                    print('SYS ERROR DEBUG:')
                    print(sys.exc_info())
                    print('ERROR QUERY:')
                    print(self.query)
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

    def response(self, is_success, message_success=None, message_failure=None, points=None, is_sys_fail=None):
        if is_success:
            if message_success is None:
                message_statement = 'Correct'
            elif self.custom_feedback is not None:
                message_statement = {"test_type": "custom",
                                     "test_key": "custom_feedback",
                                     "params": [self.custom_feedback]}
            else:
                message_statement = message_success
        else:
            if message_failure is None:
                message_statement = 'Wrong'
            elif self.custom_feedback is not None:
                message_statement = {"test_type": "custom",
                                     "test_key": "custom_feedback",
                                     "params": [self.custom_feedback]}
            else:
                message_statement = message_failure
        if self.debug is not None:
            print('\nFEEDBACK DEBUG:')
            if self.debug == 'DEBUG':
                print(f"Feedback: {message_statement}\n")
            if self.debug == 'ALL':
                if self.title is not None: print(f"title: {self.title}")
                if is_success is not None: print(f"is_success: {is_success}")
                if self.points is not None: print(f"points: {self.points}")
                if self.description is not None: print(f"description: {self.description}")
                if is_sys_fail is not None: print(f"is_sys_fail: {is_sys_fail}")
                print(f"Feedback: {message_statement}\n")

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
        if len(split_sys_feedback) > 1:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "undefined_column",
                 "params": [split_sys_feedback[1]]},
            )
        else:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "custom_feedback",
                 "params": [sysfeedback]},
            )

    def _undefined_table_error_feedback(self, sysfeedback):
        split_sys_feedback = sysfeedback.split('"')

        if len(split_sys_feedback) > 1:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "undefined_table",
                 "params": [split_sys_feedback[1]]},
            )
        else:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "custom_feedback",
                 "params": [sysfeedback]},
            )

    def _ambiguous_column_error_feedback(self, sysfeedback):
        split_sys_feedback = sysfeedback.split('"')

        if len(split_sys_feedback) > 1:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "ambiguous_column",
                 "params": [split_sys_feedback[1]]},
            )
        else:
            return self.response(
                False,
                '',
                {"test_type": "sys_fail",
                 "test_key": "custom_feedback",
                 "params": [sysfeedback]},
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

    def _llm_check(self, result):
        if not self.should_exist and len(result) > 0:
            if self.custom_feedback is None:
                raise Exception({'test_type': 'custom', 'test_key': 'llm_check_fail'})
            else:
                raise Exception({'test_type': 'custom', 'test_key': 'custom_feedback',
                                 "params": [self.custom_feedback]})
        if self.should_exist and len(result) == 0:
            if self.custom_feedback is None:
                raise Exception({'test_type': 'custom', 'test_key': 'llm_check_fail'})
            else:
                raise Exception({'test_type': 'custom', 'test_key': 'custom_feedback',
                                 "params": [self.custom_feedback]})

    def resolve_object_name(self, expected_name, available_objects, object_resolvers):

        # 1. Correct name always has highest priority
        if expected_name in available_objects:
            return expected_name

        resolver = object_resolvers.get(expected_name, {})

        # 2. Known fallback names
        for fallback in resolver.get("fallbacks", []):
            if fallback in available_objects:
                return fallback

        # 3. Regex
        pattern = resolver.get("pattern")

        if pattern is not None:
            matches = [
                object_name
                for object_name in available_objects
                if re.fullmatch(pattern, object_name, re.IGNORECASE)
            ]

            if len(matches) == 1:
                return matches[0]

        # 4. Position
        position = resolver.get("position")

        if position is not None:
            for object_name, object_position in available_objects.items():
                if object_position == position:
                    return object_name

        return None
