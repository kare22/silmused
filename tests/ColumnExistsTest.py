import sys

from tests.TestDefinition import TestDefinition


class ColumnExistsTest(TestDefinition):
    def __init__(self, name, column_name, should_exist=True, where=None, description=None, points=0):
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{name}' AND column_name = '{column_name}'"

        if where is not None:
            query += f" AND ({where})"

        super().__init__(
            name=name,
            points=points,
            description=description,
            query=query,
        )

        self.column_name = column_name
        self.where = where
        self.should_exist = should_exist

    def execute(self, cursor):
        try:
            cursor.execute(self.query)
            result = cursor.fetchall()

            if self.should_exist:
                return super().response(
                    len(result) > 0,
                    f"Correct, column {self.column_name} found in {self.name}",
                    f"Expected to find column {self.column_name} but none were found in {self.name}",
                )
            else:
                return super().response(
                    len(result) == 0,
                    f"Correct no column named {self.column_name} found in {self.name}",
                    f"Expected to not find column {self.column_name} in {self.name}",
                )
        except:
            # TODO better handler for rollback?
            # TODO better error message?
            print(sys.exc_info())  # TODO only for testing purposes

            cursor.execute('ROLLBACK')
            return super().response(
                False,
                message_failure=sys.exc_info()
            )
