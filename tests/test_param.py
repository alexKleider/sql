#!/usr/bin/env python3

# File: tests/test_param.py

import unittest
from parameterized import parameterized

def multiply(a, b):
    return a * b

class TestMultiply(unittest.TestCase):
    @parameterized.expand([
        ("positive_numbers", 2, 3, 6),
        ("negative_numbers", -2, 3, -6),
        ("zero", 0, 5, 0),
    ])
    def test_multiply_numbers(self, name, a, b, expected):
        self.assertEqual(multiply(a, b), expected)

if __name__ == "__main__":
    unittest.main()
