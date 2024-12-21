from silmused.tests.TestDefinition import TestDefinition


class IndexTest(TestDefinition):
    def __init__(self, name, title=None, description=None, custom_feedback=None, points=0):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            custom_feedback=custom_feedback,
            query=f"SELECT * FROM pg_indexes WHERE indexname = '{name}'",
        )

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.custom_feedback is None:
            return super().response(
                len(result) > 0,
                {"test_type": "index_test",
                 "test_key": "index_positive_feedback",
                 "params": [self.name]},
                {"test_type": "index_test",
                 "test_key": "index_negative_feedback",
                 "params": [self.name]}
            )
        else:
            return super().response(
                len(result) > 0,
                {"test_type": "index_test",
                 "test_key": "custom_feedback",
                 "params": [self.custom_feedback]},
                {"test_type": "index_test",
                 "test_key": "custom_feedback",
                 "params": [self.custom_feedback]},
            )