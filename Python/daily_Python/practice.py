class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

class LineCounterWorker(Worker):
    def map(self):
        data = self.input_data.read()