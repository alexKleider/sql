#!/usr/bin/env python3

# File: tests/test_helpers.py

import sys
import os
# sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
import json
import shutil
import unittest
from code import helpers

"""
To consider in the future:
    helpers is a module shared by several code bases
    so tests should probably be elsewhere.

Only a tiny fraction of the code is tested.
Suggested priority for writing test code:
    helpers.get_int
"""

class TestAdd2json(unittest.TestCase):

    a_dict = [{"A": "alex", "J": "June", }]
    a_as_str = '[{"A": "alex", "J": "June"}]'
    b_dict = {'BC': 'Cavin Rd', 'USA': 'Bolinas', }
    b_as_str  = '{"BC": "Cavin Rd", "USA": "Bolinas"}'
    c_dict = {"name": 'Alex Kleider', 'phone': '650/269-8936',}
    c_as_str = '{"name": "Alex Kleider", "phone": "650/269-8936"}'
    d_dict = {'first': 'Alex', 'last': 'Kleider', 'bday': '19450703', }
    d_as_str = '{"first": "Alex", "last": "Kleider", "bday": "19450703"}'
    pairs = [
            (a_dict, a_as_str, "tests/temp0.json"),
            (b_dict, b_as_str, "tests/temp1.json"),
            (c_dict, c_as_str, "tests/temp2.json"),
            (d_dict, d_as_str, "tests/temp3.json"),
            ]
    
    def setUp(self):
        """
        dump dict into 'jfile'
        """
        for d, s, f in self.pairs:
            with open(f, 'w', encoding='utf-8') as stream:
                json.dump(d, stream)

    def test_l(self):
        for d, s, f in self.pairs:
            self.assertEqual(helpers.content(f), s)

    def tearDown(self):
        for d, s, f in self.pairs:
            if os.path.exists(f):
                os.remove(f)


# result lists
answers=dict(
false_true=[
    "first: Alex",
    "last: Kleider",
    "payment: 200",
    "personID: 145",
    ],
false_false=[
    "personID: 145",
    "first: Alex",
    "last: Kleider",
    "payment: 200",
    ],
true_true=[
    'first\n\tAlex\n',
    'last\n\tKleider\n',
    'payment\n\t200\n',
    'personID\n\t145\n',
    ],
true_false=[
    "personID\n\t145\n",
    "first\n\tAlex\n",
    "last\n\tKleider\n",
    "payment\n\t200\n"
    ],
)

class Test_Show_Dict(unittest.TestCase):

    def setUp(self):
        self.data = {}
        self.data['personID'] = 145
        self.data['first'] = "Alex"
        self.data['last'] = "Kleider"
        self.data['payment'] = 200

    def test_show_dict_true_true(self):
        self.assertEqual(
            helpers.show_dict(self.data),
            answers["true_true"])
            
    def test_show_dict_true_false(self):
        self.assertEqual(
            helpers.show_dict(self.data,
                                extra_line=True,
                                ordered=False),
            answers["true_false"])
      
    def test_show_dict_false_true(self):
        self.assertEqual(
            helpers.show_dict(self.data,
                                extra_line=False,
                                ordered=True),
            answers["false_true"])
       
    def test_show_dict_false_false(self):
        self.assertEqual(
            helpers.show_dict(self.data,
                                extra_line=False,
                                ordered=False),
            answers["false_false"])
        
    def tearDown(self):
        self.data = {}

if __name__ == '__main__':
    unittest.main()

