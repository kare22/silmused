class TitleLayer:
    def __init__(self, title):
        self.title = title

    def run(self, any):
        return {
            'type': 'title',
            'message': self.title
        }