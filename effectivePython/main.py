class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


def add_book(queue, book):
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True)

queue = []
add_book(queue, Book('돈키호테', '2020-06-07'))
add_book(queue, Book('프랑켄슈타인', '2020-06-05'))
add_book(queue, Book('레미제라블', '2020-06-08'))
add_book(queue, Book('전쟁과 평화', '2020-06-03'))

class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book
    raise NoOverdueBooks

now = '2020-06-10'
found = next_overdue_book(queue, now)
print(found.title)

found = next_overdue_book(queue, now)
print(found.title)


def return_book(queue, book):
    queue.remove(book)

queue = []
book = Book('보물섬', '2020-06-04')

add_book(queue, book)
print('반납 전', [x.title for x in queue])

return_book(queue, book)
print('반납 후', [x.title for x in queue])


try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass
else:
    assert False

from heapq import heappush

def add_book(queue, book):
    heappush(queue, book)

queue = []
add_book(queue, Book('작은 아씨들', '2020-06-05'))
add_book(queue, Book('타임 머신', '2020-05-30'))

import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date

queue = []
add_book(queue, Book('돈키호테', '2020-06-07'))
add_book(queue, Book('프랑켄슈타인', '2020-06-05'))
add_book(queue, Book('레미제라블', '2020-06-08'))
add_book(queue, Book('전쟁과 평화', '2020-06-03'))

queue = [
Book('돈키호테', '2020-06-07'),
Book('프랑켄슈타인', '2020-06-05'),
Book('레미제라블', '2020-06-08'),
Book('전쟁과 평화', '2020-06-03'),
]

queue.sort()

from heapq import heapify

queue = [
    Book('돈키호테', '2020-06-07'),
    Book('프랑켄슈타인', '2020-06-05'),
    Book('레미제라블', '2020-06-08'),
    Book('전쟁과 평화', '2020-06-03'),
]
heapify(queue)

from heapq import heappop
def next_overdue_book(queue, now):
    if queue:
        book = queue[0]
        if book.due_date < now:
            heappop(queue)
            return book
    raise NoOverdueBooks

now = '2020-06-02'
book = next_overdue_book(queue, now)
print(book.title)

book = next_overdue_book(queue, now)
print(book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass
else:
    assert False

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False