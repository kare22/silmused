from silmused.tests.TestDefinition import TestDefinition


class IndexTest(TestDefinition):
    def __init__(self, name, title=None, description=None, points=0):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            query=f"SELECT * FROM pg_indexes WHERE indexname = '{name}'",
        )

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()

        return super().response(
            len(result) > 0,
            {"test_type": "index_test",
             "test_key": "index_positive_feedback",
             "params": [self.name]},
            {"test_type": "index_test",
             "test_key": "index_negative_feedback",
             "params": [self.name]}
        )