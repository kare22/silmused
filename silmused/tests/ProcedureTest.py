from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class ProcedureTest(TestDefinition):
    def __init__(self, name, arguments, title=None, number_of_columns=None, description=None, expected_value=None, expected_count=None, pre_query=None, after_query=None, points=0):
        if after_query is None:
            raise Exception('Parameter "after_query" is required')

        super().__init__(
            name=name,
            title=title,
            points=points,
            arguments=arguments,
            description=description,
            expected_value=expected_value,
            expected_count=expected_count,
            pre_query=pre_query,
            query=f"CALL {name}({list_to_string(arguments)})",
            after_query=after_query,
        )

        self.number_of_columns = number_of_columns

    def execute(self, cursor):
        if self.number_of_columns is not None:
            cursor.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname = '{self.name}'")
            if not cursor.fetchall()[0][0] == self.number_of_columns:
                return False, f"Procedure's \"{self.name}\" number of parameters is wrong",

        if self.pre_query is not None:
            cursor.execute(self.pre_query)

        cursor.execute(self.query)

        cursor.execute(self.after_query)

        result = cursor.fetchall()

        return super().response(
            len(result) > 0,
            f"Correct count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\"",
            f"Expected count > 0 for procedure \"{self.name}({list_to_string(self.arguments)})\" but none was found",
        )