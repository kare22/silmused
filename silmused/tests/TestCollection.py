import sys


# TODO this should not be usable without a child
class TestCollection:
    def __init__(self, title, points, cases=None):
        self.title = title
        self.points = points
        self.cases = cases
        if cases is not None and not isinstance(cases, list):
            raise Exception('Collection of tests cannot be empty.') 