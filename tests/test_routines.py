#!/usr/bin/env python3

# File: tests/test_routines.py

import sys
import os
import unittest
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import routines

"""
Only a tiny fraction of the code is tested.
Suggested priority for writing test code:
    --
"""

class Test_keys_from_schema(unittest.TestCase):

    def test_default(self):
        keys = routines.keys_from_schema("People")
        self.assertEqual(keys, 
            routines.keys_from_schema("People",brackets=(0,0)))
        for begin,end in ((0,0), (1,0), (2,1), (0, 3),):
            ending = len(keys) - end
            self.assertEqual(keys[begin:ending], 
                routines.keys_from_schema("People",
                    brackets=(begin,end)))
            pass
        pass

if __name__ == '__main__':
    unittest.main()
