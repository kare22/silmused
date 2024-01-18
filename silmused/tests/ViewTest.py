from silmused.tests.TestDefinition import TestDefinition


# TODO Right now it is only possible to check the existence of a view
# Probably there is no need for this as it is covered by table tests

# We can use it to test the existence of materialized views
class ViewTest(TestDefinition):
    def __init__(self, name, title=None, description=None, points=0):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            query=f"SELECT * FROM information_schema.views WHERE table_name = '{name}'",
        )

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        return super().response(
            len(result) > 0,
            f"Correct, view {self.name} found",
            f"Expected to find view {self.name} but none were found",
        )