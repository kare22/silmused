from silmused.tests.TestDefinition import TestDefinition


# TODO raname to TableDataTest ??
class DataTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, should_exist=True, where=None, join=None, description=None,
                 expected_value=None, points=0):

        if column_name is not None and not isinstance(column_name, str):
            raise Exception('Parameter "column_name" must be a string')

        super().__init__(
            name=name,
            title=title,
            where=where,
            join=join,
            points=points,
            description=description,
            query=f"SELECT {column_name if column_name is not None else '*'} FROM {name}",
            should_exist=should_exist,
            expected_value=expected_value,
        )

        self.column_name = column_name
        self.where = where
        self.join = join

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        if self.expected_value is None:
            if self.should_exist:
                return super().response(
                    len(result) > 0,
                    f"Correct, results found for table {self.name} and column(s) {self.column_name}",
                    f"Expected to find results for table {self.name} and column(s) {self.column_name} but none were found",
                )
            else:
                return super().response(
                    len(result) == 0,
                    f"Correct, no results found for table {self.name} and column(s) {self.column_name} ",
                    f"Expected to find nor results for table {self.name} and column(s) {self.column_name} but some were found",
                )
        else:
            if self.should_exist:
                # TODO add type check

                return super().response(
                    str(result[0][0]) == str(self.expected_value),
                    f"Correct value found for table {self.name} and column(s) {self.column_name}",
                    f"Expected to find {self.expected_value} for table {self.name} and column(s) {self.column_name} but found {result[0][0]}",
                )
            else:
                return super().response(
                    str(result[0][0]) != str(self.expected_value),
                    f"Correct, {self.expected_value} does not equal {result[0][0]} in  table {self.name} and column(s) {self.column_name} ",
                    f"Expected {self.expected_value} to not equal {result[0][0]} in table {self.name} and column(s) {self.column_name}",
                )
