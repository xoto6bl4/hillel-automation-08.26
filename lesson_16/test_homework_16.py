"""Tests for the lesson 16 generators, iterators, and decorators."""

import unittest
from types import GeneratorType

from homework_16 import (
    EvenNumbersIterator,
    ReverseListIterator,
    even_numbers,
    fibonacci_up_to,
    handle_exceptions,
    log_calls,
)


class Homework16Tests(unittest.TestCase):
    def test_even_generator_includes_zero_and_upper_bound(self):
        self.assertIsInstance(even_numbers(4), GeneratorType)
        self.assertEqual(list(even_numbers(4)), [0, 2, 4])
        self.assertEqual(list(even_numbers(5)), [0, 2, 4])
        self.assertEqual(list(even_numbers(0)), [0])
        self.assertEqual(list(even_numbers(-1)), [])

    def test_fibonacci_generator_includes_limit(self):
        self.assertIsInstance(fibonacci_up_to(8), GeneratorType)
        self.assertEqual(list(fibonacci_up_to(8)), [0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(list(fibonacci_up_to(4)), [0, 1, 1, 2, 3])
        self.assertEqual(list(fibonacci_up_to(0)), [0])
        self.assertEqual(list(fibonacci_up_to(-1)), [])

    def test_reverse_list_iterator_and_exhaustion(self):
        iterator = ReverseListIterator([1, 2, 3])
        self.assertIs(iter(iterator), iterator)
        self.assertEqual(next(iterator), 3)
        self.assertEqual(list(iterator), [2, 1])
        with self.assertRaises(StopIteration):
            next(iterator)
        self.assertEqual(list(ReverseListIterator([])), [])

    def test_even_iterator_and_exhaustion(self):
        iterator = EvenNumbersIterator(4)
        self.assertIs(iter(iterator), iterator)
        self.assertEqual(next(iterator), 0)
        self.assertEqual(list(iterator), [2, 4])
        with self.assertRaises(StopIteration):
            next(iterator)
        self.assertEqual(list(EvenNumbersIterator(5)), [0, 2, 4])
        self.assertEqual(list(EvenNumbersIterator(-1)), [])

    def test_log_calls_preserves_result_metadata_and_logs_arguments(self):
        @log_calls
        def add(a, b=0):
            """Add two numbers."""
            return a + b

        with self.assertLogs('homework_16', level='INFO') as captured:
            self.assertEqual(add(2, b=3), 5)
        self.assertEqual(add.__name__, 'add')
        self.assertEqual(add.__doc__, 'Add two numbers.')
        self.assertIn("args=(2,), kwargs={'b': 3}", captured.output[0])
        self.assertIn('add returned 5', captured.output[1])

    def test_handle_exceptions_returns_value_or_logs_failure(self):
        @handle_exceptions
        def divide(a, b):
            return a / b

        self.assertEqual(divide(6, 2), 3)
        with self.assertLogs('homework_16', level='ERROR') as captured:
            self.assertIsNone(divide(6, 0))
        self.assertIn('Error in divide', captured.output[0])
        self.assertIn('ZeroDivisionError', captured.output[0])
        self.assertEqual(divide.__name__, 'divide')


if __name__ == '__main__':
    unittest.main()