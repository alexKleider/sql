#!/usr/bin/env python3

# File: tests/test_utils_scan.py

import unittest
from utils import scan


class TestUtilsScan(unittest.TestCase):

    def test_find_words_in_line(self):
        target = "lib.func"
        test_cases = [
                ("mylib.func(", []),
                ("lib.func(", [0]),
                (" lib.func( ", [1]),
                ("(lib.func(param) ", [1]),
                (" lib.func(param1)  lib.func(param2)", [1, 19]),
                ("just random text", []),
                ("", []),
                ("   ", []),
                ("hellolib.func", []),
                ("def lib.function(", []),
                ("some stuff lib.func() and again lib.func(  ", [11,
                                                                 32]),
                (" some code lib.func_extra", []),
                (" some codelib.func(_extra", []),
                ]
        print()
        for line, res in test_cases:
            print((line, res))
            self.assertEqual(
                scan.find_words_in_line(target, line), res)

    def test_find(self):
        self.assertTrue(True)

    def test_find_func_def(self):
        test_cases = [
                ("   def func1(param1, param2):", 'func1'),
                ("def func2(params):  #", 'func2'),
                ]
        for line, res in test_cases:
            self.assertEqual(scan.find_func_def(line), res)

    def test_module_name(self):
        test_cases = [
            ("code/alchemy.py", "alchemy"),
            ("junk/junk.py", "junk"),
            ]
        for s_name, m_name in test_cases:
            self.assertEqual(scan.module_name(s_name), m_name)

    def test_show(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

