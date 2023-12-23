import sys

from tests.TestDefinition import TestDefinition


# Right now it is only possible to check the existence of a view
class ViewTest(TestDefinition):
    def __init__(self, name, description=None, points=0):
        query = f"SELECT * FROM information_schema.views WHERE table_name = '{name}'"

        super().__init__(
            name=name,
            points=points,
            description=description,
            query=query,
        )

    def execute(self, cursor):
        try:
            cursor.execute(self.query)
            result = cursor.fetchall()

            return super().response(
                len(result) > 0,
                f"Correct, view {self.name} found",
                f"Expected to find view {self.name} but none were found",
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
