from tests.TestDefinition import TestDefinition


class ColumnExistsTest(TestDefinition):
    def __init__(self, name, column_name, should_exist=True, where=None, description=None, points=0):
        if not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if column_name is None:
            raise Exception('Parameter "column_name" is required')

        super().__init__(
            name=name,
            where=where,
            points=points,
            description=description,
            query=f"SELECT * FROM information_schema.columns WHERE table_name = '{name}' AND column_name = '{column_name}'",
            should_exist=should_exist,
        )

        self.column_name = column_name
        self.where = where

    def execute(self, cursor):
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
