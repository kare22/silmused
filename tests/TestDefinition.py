from utils import list_to_string


# TODO this should not be usable without a child
class TestDefinition:
    def __init__(self, name, points, arguments, expected_value=None, expected_count=None):
        if not isinstance(arguments, list):
            raise Exception('Parameter "arguments" must be a list')

        if expected_count is not None and not isinstance(expected_count, int):
            raise Exception('Parameter "expected_count" must be an integer')

        if not isinstance(points, int) and not isinstance(points, float):
            raise Exception('Parameter "points" must be either an integer or a float')

        if expected_value is not None and expected_count is not None:
            raise Exception('Both expected_value and check_count cannot be specified in a single test')

        self.name = name
        self.points = points
        self.type = "generic"
        self.arguments = list_to_string(arguments)
        self.expected_value = expected_value
        self.expected_count = expected_count

    def execute(self, cursor):
        raise NotImplementedError('Method "execute" not implemented')

    # TODO should be callable only inside the scope
    def response(self, is_success, message_success=None, message_failure=None):
        if is_success:
            message_statement = 'Correct' if message_success is None else message_success
        else:
            message_statement = 'Wrong' if message_failure is None else message_failure

        return {
            'is_success': is_success,
            'message': message_statement,
            'points': self.points,
        }

    def __str__(self):
        return f"Test({self.name}, Type: {self.type}, Points: {self.points})"
