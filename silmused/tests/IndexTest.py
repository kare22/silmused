from silmused.tests.TestDefinition import TestDefinition


class IndexTest(TestDefinition):
    def __init__(self, name, title=None, description=None, custom_feedback=None, debug=None, points=0):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            custom_feedback=custom_feedback,
            query=f"SELECT * FROM pg_indexes WHERE indexname = '{name}'",
            debug=debug,
        )
        self.test_type = "index_test"

    def execute(self, cursor):
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.debug is not None: self.debug_output(result)

        # Result Assessment
        return super().response(
            len(result) > 0,
            {"test_type": self.test_type,
             "test_key": "index_positive_feedback",
             "params": [self.name]},
            {"test_type": self.test_type,
             "test_key": "index_negative_feedback",
             "params": [self.name]}
        )

    def debug_output(self, result):
        print('INDEX TEST DEBUG: ')
        if self.debug == 'DEBUG':
            if self.title is not None: print(f"Test title: {self.title}")
            print(f"query: {self.query}")
            print(f"result: {result}")
        if self.debug == 'ALL':
            if self.name is not None: print(f"name: {self.name}")
            if self.description is not None: print(f"description: {self.description}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.test_type is not None: print(f"test_type: {self.test_type}")
        if self.debug != 'DEBUG' or self.debug != 'ALL':
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")