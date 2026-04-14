from dispatcher import QueryDispatcher

class UDCPRAgent:

    def __init__(self):
        self.dispatcher = QueryDispatcher()

    def run(self, query, project_data):
        return self.dispatcher.process(query, project_data)
