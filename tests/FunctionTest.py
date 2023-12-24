from tests.TestDefinition import TestDefinition
from utils import list_to_string


class FunctionTest(TestDefinition):
    def __init__(self, name, arguments, where=None, description=None, expected_value=None, expected_count=None, points=0):
        super().__init__(
            name=name,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            query=f"SELECT * FROM {name}({list_to_string(arguments)})"  # TODO implement parameters,
        )

    def execute(self, cursor):
        # TODO should the following be optional or added natively? ->
        # TODO * Check that function name exists
        # TODO * Check that function number of arguments is correct
        # TODO * Check that type is correct
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.expected_value is None:
            if self.expected_count is None:
                return super().response(
                    len(result) > 0,
                    f"Correct count > 0 for function {self.name}({self.arguments})",
                    f"Expected count > 0 for function {self.name}({self.arguments}) but none was found",
                )
            else:
                return super().response(
                    len(result) == self.expected_count,
                    f"The count is correct for function {self.name}({self.arguments}) -> {self.expected_count}",
                    f"Expected count {self.expected_count} for function {self.name}({self.arguments}) but got {len(result)}",
                )
        else:
            if type(result[0][0]) != type(self.expected_value):
                return super().response(
                    False,
                    'Correct',
                    f"Expected type {type(self.expected_value)} but got {type(result[0][0])}",
                )
            return super().response(
                result[0][0] == self.expected_value,
                'Correct',
                f"Expected {self.expected_value} but got {result[0][0]}",
            )
