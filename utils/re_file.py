#!/usr/bin/env python3

# File: re_file.py

import re
import unittest

func_po = re.compile(r"def [a-zA-Z]+[a-zA-Z0-1_]*\(")

def find_func_def(line):
    return func_po(line)  # returns None or a match object

class TestUtilsScan(unittest.TestCase):

    def test_find_func_def(self):
        test_cases = [
                ("def myfunc(param_listing):   ", "def myfunc("),
                ("just a randme line ", None),
                ]
        for line, res in test_cases:
            match = func_po.search(line)
            if not match:
                self.assertEqual(match, None)
            else:
                self.assertEqual(match.group(), res)


if __name__ == "__main__":
    unittest.main()
