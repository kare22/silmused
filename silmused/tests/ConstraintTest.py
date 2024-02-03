from silmused.tests.TestDefinition import TestDefinition


class ConstraintTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, constraint_name=None, constraint_type=None, description=None, should_exist=True, points=0):
        query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{name}'"

        if constraint_name is not None:
            query += f" AND constraint_name = '{constraint_name}'"
        if constraint_type is not None:
            query += f" AND constraint_type = '{constraint_type}'"

        super().__init__(
            name=name,
            title=title,
            column_name=column_name,
            points=points,
            description=description,
            query=query,
            should_exist=should_exist,
        )

        self.constraint_name = constraint_name
        self.constraint_type = constraint_type

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
        check_columns_result = self.check_columns(cursor)
        if check_columns_result is not None:
            return check_columns_result

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

    def check_columns(self, cursor):
        if self.column_name is None:
            return None

        query = f"SELECT * FROM information_schema.key_column_usage WHERE table_name = '{self.name}'"

        if self.constraint_name is not None:
            query += f" AND constraint_name = '{self.constraint_name}'"

        cursor.execute(query)
        result = cursor.fetchall()

        columns = [res[6] for res in result]

        print(columns)

        if type(self.column_name) == str and self.column_name in columns:
            return None
        elif type(self.column_name) == list:
            is_correct = True
            for column_name in self.column_name:
                if not column_name in columns:
                    is_correct = False
                    break
            if is_correct:
                return None

        return super().response(
            False,
            None,
            f"Expected column(s) {self.column_name} but got {columns}"
        )