from tests.TestDefinition import TestDefinition
from utils import list_to_string


class ColumnStructureTest(TestDefinition):
    def __init__(self, name, column_name, arguments=None, expected_value=None, should_exist=True, where=None, description=None, points=0):
        if not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if column_name is None:
            raise Exception('Parameter "column_name" is required')

        query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.columns WHERE table_name = '{name}' AND column_name = '{column_name}'"

        super().__init__(
            name=name,
            where=where,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            query=query,
            should_exist=should_exist,
        )

        self.column_name = column_name
        self.where = where

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.expected_value is not None:
            if self.should_exist:
                return super().response(
                    len(result) != 0 and result[0][0] == self.expected_value,
                    f"Correct, expected {self.query}", # TODO enhance feedback
                    f"Wrong, did not expect {self.query}", # TODO enhance feedback
                )
            else:
                return super().response(
                    len(result) == 0 or result[0][0] != self.expected_value,
                    f"Correct did not want {self.query}", # TODO enhance feedback
                    f"Wrong this should not exist {self.query}", # TODO enhance feedback
                )
        else:
            if self.should_exist:
                return super().response(
                    len(result) > 0,
                    f"Correct, column {self.column_name} found in table {self.name}",
                    f"Expected to find column {self.column_name} but none were found in table {self.name}",
                )
            else:
                return super().response(
                    len(result) == 0,
                    f"Correct no column named {self.column_name} found in table {self.name}",
                    f"Expected to not find column {self.column_name} in table {self.name}",
                )
