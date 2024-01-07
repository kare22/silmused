import sys


class ExecuteLayer:
    def __init__(self, query):
        self.query = query

    def run(self, cursor):
        try:
            cursor.execute(self.query)

            return {
                'type': 'execution',
                'message': 'Success',
                'query': self.query,
            }
        except:
            cursor.execute('ROLLBACK')

            return {
                'type': 'execution',
                'message': 'Failure',
                'error': sys.exc_info(),
                'query': self.query,
            }