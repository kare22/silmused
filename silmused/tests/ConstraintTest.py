from silmused.tests.TestDefinition import TestDefinition


class ConstraintTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, constraint_name=None, constraint_type=None, description=None, should_exist=True, points=0):
        query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{name}'"

        if column_name is not None:
            query += f" AND constraint_name LIKE '%{column_name}%'"
        if constraint_name is not None:
            query += f" AND constraint_name = '{constraint_name}'"
        if constraint_type is not None:
            query += f" AND constraint_type = '{constraint_type}'"

        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            query=query,
            should_exist=should_exist,
        )

        self.constraint_name = constraint_name
        self.constraint_type = constraint_type
        self.column_name = column_name

        self.feedback = f"table {self.name}"

        if self.column_name is not None:
            self.feedback += f" with column = '{self.column_name}'"
        if self.constraint_name is not None:
            self.feedback += f" with constraint name = '{self.constraint_name}'"
        if self.constraint_type is not None:
            if self.constraint_name is None:
                self.feedback += f" with constraint type = '{self.constraint_type}'"
            else:
                self.feedback += f" and type = '{self.constraint_type}'"

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.should_exist:
            return super().response(
                len(result) > 0,
                f"Correct, {self.feedback} was found",
                f"Expected to find {self.feedback} but none were found",
            )
        else:
            return super().response(
                len(result) == 0,
                f"Correct, {self.feedback} was not found",
                f"Expected to no find {self.feedback}",
            )