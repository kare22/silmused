import sys


# TODO this should not be usable without a child
class TestDefinition():
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
        self.arguments = arguments # TODO arguments could be a class
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
            return self.execute(cursor)
        except:
            # TODO better handler for rollback?
            # TODO better error message?

            cursor.execute('ROLLBACK')
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
