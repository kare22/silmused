from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class StructureTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, arguments=None, expected_value=None, should_exist=True, where=None, description=None, points=0):
        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')

        query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.columns WHERE table_name = '{name}'"

        if column_name is not None:
            query += f" AND column_name = '{column_name}'"

        super().__init__(
            name=name,
            title=title,
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
        # TODO feedback is really bad
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
                    f"Correct, column or table {self.column_name if self.column_name is not None else self.name} found in table {self.name}",
                    f"Expected to find column or table {self.column_name if self.column_name is not None else self.name} but none were found in table {self.name}",
                )
            else:
                return super().response(
                    len(result) == 0,
                    f"Correct no column or table named {self.column_name if self.column_name is not None else self.name} found in table {self.name}",
                    f"Expected to not find column or table {self.column_name if self.column_name is not None else self.name} in table {self.name}",
                )
