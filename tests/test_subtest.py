#!/usr/bin/env python3

# File: tests/test_param.py

import unittest

def add(x, y):
    return x + y

class TestAdd(unittest.TestCase):
    def test_add_numbers(self):
        test_cases = [(1, 2, 3), (-1, 1, 0), (0, 0, 0)]

        for x, y, expected in test_cases:
            with self.subTest(x=x, y=y):
                self.assertEqual(add(x, y), expected)

if __name__ == '__main__':
    unittest.main()

