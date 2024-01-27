from uuid import uuid4


class ChecksLayer:
    def __init__(self, title=f"test_{str(uuid4())}", tests=[]):
        self.title = title
        self.tests = tests

    def run(self, cursor):
        results = []
        for test in self.tests:
            results.append(test.run(cursor))

        return {
            'title': self.title,
            'type': 'checks_layer',
            'checks': results,
        }
