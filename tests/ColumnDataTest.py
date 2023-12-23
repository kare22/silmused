import sys

from tests.TestDefinition import TestDefinition


class ColumnDataTest(TestDefinition):
    def __init__(self, name, column_name, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, points=0):
        if not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')
        if column_name is None:
            raise Exception('Parameter "column_name" is required')

        query = f"SELECT {column_name} FROM {name}"

        # TODO right now a single join is possible (without a hack)
        if join is not None:
            query += f" JOIN {join}"

        if where is not None:
            query += f" AND ({where})"

        super().__init__(
            name=name,
            points=points,
            description=description,
            query=query,
            should_exist=should_exist,
            expected_value=expected_value,
        )

        self.column_name = column_name
        self.where = where
        self.join = join

    def execute(self, cursor):
        try:
            cursor.execute(self.query)
            result = cursor.fetchall()

            if self.expected_value is None:
                if self.should_exist:
                    return super().response(
                        len(result) > 0,
                        f"Correct, results found for table {self.name} and column {self.column_name}",
                        f"Expected to find results for table {self.name} and column {self.column_name} but none were found",
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        f"Correct, no results found for table {self.name} and column {self.column_name} ",
                        f"Expected to find nor results for table {self.name} and column {self.column_name} but some were found",
                    )
            else:
                if self.should_exist:
                    # TODO add type check

                    return super().response(
                        result[0][0] == self.expected_value,
                        f"Correct value found for table {self.name} and column {self.column_name}",
                        f"Expected to find {self.expected_value} for table {self.name} and column {self.column_name} but found {result[0][0]}",
                    )
                else:
                    return super().response(
                        result[0][0] != self.expected_value,
                        f"Correct, {self.expected_value} does not equal {result[0][0]} in  table {self.name} and column {self.column_name} ",
                        f"Expected {self.expected_value} to not equal {result[0][0]} in table {self.name} and column {self.column_name}",
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
