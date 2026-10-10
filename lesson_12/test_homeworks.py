import unittest

from homeworks import (
    calculate_total_area,
    check_symbols,
    has_h_letter,
    sum_even_numbers,
    str_inside_out
)


class TestCalculateTotalArea(unittest.TestCase):

    def test_total_area(self):
        result = calculate_total_area(436402, 37800)
        self.assertEqual(result, 474202)

    def test_total_area_with_zero(self):
        result = calculate_total_area(436402, 0)
        self.assertEqual(result, 436402)


class TestCheckSymbols(unittest.TestCase):

    def test_more_than_10_symbols(self):
        result = check_symbols("abcdefghijk")
        self.assertTrue(result)

    def test_10_or_less_symbols(self):
        result = check_symbols("abcdefghij")
        self.assertFalse(result)


class TestHasHLetter(unittest.TestCase):

    def test_has_h_letter(self):
        result = has_h_letter("Hello")
        self.assertTrue(result)

    def test_has_no_h_letter(self):
        result = has_h_letter("World")
        self.assertFalse(result)


class TestSumEvenNumbers(unittest.TestCase):

    def test_sum_even_numbers(self):
        result = sum_even_numbers([16, 3, 33, 55, 44, 10, 77])
        self.assertEqual(result, 70)

    def test_no_even_numbers(self):
        result = sum_even_numbers([1, 3, 5, 7, 9])
        self.assertEqual(result, 0)


class TestStrInsideOut(unittest.TestCase):

    def test_reverse_string(self):
        result = str_inside_out("Forza Ferrari")
        self.assertEqual(result, "irarreF azroF")

    def test_one_character(self):
        result = str_inside_out("A")
        self.assertEqual(result, "A")


if __name__ == "__main__":
    unittest.main()