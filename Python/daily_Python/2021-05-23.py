#- classmethod를 활용하여 제너릭하게 코드 구현 예제

#- 코드 예제
#- inputData, thread를 이용한 mapreduce 처리하기

import os
from threading import Thread
import random


class GenericInputData:
    def __init__(self, path):
        self.path = path

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):

    def read(self):
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))

        return workers


class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    # - first worker를 기준으로 reduce 연산 수행
    first, * rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


tmpdir = 'test_dir'
os.mkdir(tmpdir)
for i in range(100):
    with open(os.path.join(tmpdir, str(i)), 'w') as f:
        f.write('\n' * random.randint(0, 100))

config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
