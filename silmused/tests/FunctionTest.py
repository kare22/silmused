from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class FunctionTest(TestDefinition):
    def __init__(self, name, title=None, arguments=None, column_name=None, where=None, description=None, expected_value=None, expected_count=None, number_of_parameters=None, points=0):
        super().__init__(
            name=name,
            title=title,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            query=f"SELECT {column_name if column_name is not None else '*'} FROM {name}({list_to_string(arguments if arguments is not None else '')})"  # TODO implement parameters,
        )

        self.number_of_parameters = number_of_parameters

    def execute(self, cursor):
        # TODO small tests in separate functions

        # Check that function name exists
        cursor.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{self.name}'")
        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                ''
                f"Function {self.name} was not found"
            )

        # Check that function number of arguments is correct
        if self.number_of_parameters is not None:
            cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname='{self.number_of_parameters}'")
            number_of_parameters_result = cursor.fetchall()[0][0]

            if not number_of_parameters_result == self.number_of_parameters:
                return super().response(
                    False,
                    ''
                    f"Expected {self.number_of_parameters} for function {self.name} but found {number_of_parameters_result}"
                )
        # Check that type is correct
        cursor.execute(f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION' AND routine_name='{self.name}'")
        if not len(cursor.fetchall()) > 0:
            return super().response(
                False,
                ''
                f"Expected function {self.name} to be of type FUNCTION"
            )

        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.expected_value is None:
            if self.expected_count is None:
                return super().response(
                    len(result) > 0,
                    f"Correct count > 0 for function {self.name}({list_to_string(self.arguments)})",
                    f"Expected count > 0 for function {self.name}({list_to_string(self.arguments)}) but none was found",
                )
            else:
                return super().response(
                    len(result) == self.expected_count,
                    f"The count is correct for function {self.name}({list_to_string(self.arguments)}) -> {self.expected_count}",
                    f"Expected count {self.expected_count} for function {self.name}({list_to_string(self.arguments)}) but got {len(result)}",
                )
        else:
            # TODO when type is decimal but we give float, we get an error
            # if type(result[0][0]) != type(self.expected_value):
            #     return super().response(
            #         False,
            #         'Correct',
            #         f"Expected type {type(self.expected_value)} but got {type(result[0][0])}",
            #     )
            return super().response(
                str(result[0][0]) == str(self.expected_value),
                'Correct',
                f"Expected {self.expected_value} but got {result[0][0]}",
            )
