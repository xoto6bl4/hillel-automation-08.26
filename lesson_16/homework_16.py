"""Lesson 16: generators, iterators, and decorators."""

import logging
from functools import wraps


logger = logging.getLogger(__name__)


def even_numbers(n):
    """Yield even numbers from 0 through n, inclusive."""
    for number in range(0, n + 1, 2):
        yield number


def fibonacci_up_to(n):
    """Yield Fibonacci numbers no greater than n (starting with 0, 1)."""
    current, following = 0, 1
    while current <= n:
        yield current
        current, following = following, current + following


class ReverseListIterator:
    """Iterate through a list from its last element to its first."""

    def __init__(self, items):
        self._items = items
        self._index = len(items) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < 0:
            raise StopIteration
        item = self._items[self._index]
        self._index -= 1
        return item


class EvenNumbersIterator:
    """Iterate over even numbers from 0 through n, inclusive."""

    def __init__(self, n):
        self._limit = n
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current > self._limit:
            raise StopIteration
        number = self._current
        self._current += 2
        return number


def log_calls(func):
    """Log a function's arguments and return value."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Calling %s: args=%r, kwargs=%r", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.info("%s returned %r", func.__name__, result)
        return result

    return wrapper


def handle_exceptions(func):
    """Log exceptions raised by a function and return None on failure."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception("Error in %s", func.__name__)
            return None

    return wrapper


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    @log_calls
    def add(a, b):
        return a + b

    @handle_exceptions
    def divide(a, b):
        return a / b

    print("Even generator:", list(even_numbers(10)))
    print("Fibonacci generator:", list(fibonacci_up_to(10)))
    print("Reverse iterator:", list(ReverseListIterator([1, 2, 3])))
    print("Even iterator:", list(EvenNumbersIterator(10)))
    print("Logged call:", add(2, 3))
    print("Handled exception:", divide(2, 0))