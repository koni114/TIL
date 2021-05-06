def america_travel_normalize(num_list):
    total = sum(num_list)
    result = []
    for num in num_list:
        result.append(100 * num / total)
    return result


visits = [15, 35, 80]
percentages = america_travel_normalize(visits)
print(percentages)
print(sum(percentages))


def read_visits(file_path):
    with open(file_path) as f:
        for line in f:
            yield int(line)

def get_iter():
    return read_visits('test.txt')

it = read_visits('test.txt')
print(next(it))
print(next(it))


percentages = america_travel_normalize(it)
print(percentages)

it = read_visits('test.txt')

def america_travel_normalize_copy(num_list):
    num_list_copy = list(num_list)
    total = sum(num_list_copy)
    result = []
    for num in num_list_copy:
        result.append(100 * num / total)
    return result

it = read_visits('test.txt')
percentages = america_travel_normalize_copy(it)
print(percentages)
assert sum(percentages) == 100

def normalize_func(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result



def get_iter():
    return read_visits('test.txt')


percentages = normalize_func(lambda: read_visits('test.txt'))

#- Counter 라는 Iterable 객체
#- Counter_Iterator 라는 Iterator 객체
class Counter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop:
            return_value = self.current
            self.current += 1
            return return_value
        else:
            raise StopIteration

counter_iterator = iter(Counter(5))
print(next(counter_iterator))

class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):
        raise TypeError("컨테이너를 제공해야 합니다.")
    total = sum(numbers)
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result


percentages = normalize_defensive(numbers=visits)
percentages = normalize_defensive(numbers=ReadVisits('test.txt'))
print(percentages)

value = [len(x) for x in open('test.txt')]
print(value)

it = (len(x) for x in open('test.txt'))
print(it)

roots = ((x, x**0.5) for x in it)
next(roots)


def move(period, speed):
    for _ in range(period):
        yield speed


def pause(delay):
    for _ in range(delay):
        yield 0


def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


def render(delta):
    print(f"Delta: {delta:.1f}")


def run(func):
    for delta in func():
        render(delta)


def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate_composed)


import timeit
def child():
    for i in range(1_000_000):
        yield i

def slow():
    for i in child():
        yield

def fast():
    yield from child()

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f"수동 내포: {baseline:2f}s")

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f"합성 사용: {comparison:2f}s")

reduction = (baseline - comparison) / baseline
print(f"{reduction:.1%} 시간이 적게 듬")
