#!/usr/bin/env python3

# File: tests/test_helpers.py

import sys
import os
import unittest
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import helpers

"""
Only a tiny fraction of the code is tested.
Suggested priority for writing test code:
    helpers.get_int
"""

def main():
    data = {}
    data['personID'] = 145
    data['first'] = "Alex"
    data['last'] = "Kleider"
    data['payment'] = 200
    for line in helpers.show_dict(data,
                    extra_line = False,
                    ordered = False,
                    debug = False):
        print(line)
    return
    data[''] = None
    data[''] = None
    data[''] = None
    data[''] = None
    data[''] = None
    data[''] = None

if __name__ == '__main__':
    main()

