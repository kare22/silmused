import sys


class ExecuteLayer:
    def __init__(self, query, debug=None):
        self.query = query
        self.debug = debug

    def run(self, cursor):
        try:
            cursor.execute(self.query)

            if self.debug is not None: print(f"query: {self.query}")

            return {
                'type': 'execution',
                'message': 'Success',
                'query': self.query,
            }
        except:
            cursor.execute('ROLLBACK')

            if self.debug is not None: print(f"sys_error: {sys.exc_info()}")

            return {
                'type': 'execution',
                'message': 'Failure',
                'error': sys.exc_info(),
                'query': self.query,
            }