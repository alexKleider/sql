#!/usr/bin/env python3

# File: tests/test_helpers.py

import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
import json
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

def code2test_add2json_file():
    """
    Needs work! 
    Need to mv Secret/jfile.json to tests directory
    and have a setUp routine to cp it to something for testing
    and then be "tearDown"ed afterwards
    """
    jfile = "Secret/jfile.json"

    l = [{'A': 'alex', 'J': 'June', }]
    d = {'BC': 'Cavin Rd', 'USA': 'Bolinas', }
    d2 = {"name": 'Alex Kleider', 'phone': '650/269-8936',}
    d3 = {'first': 'Alex', 'last': 'Kleider', 'bday': '19450703', }

    for1stTimeOnly = """
    response = input("Initialize the json file? (y/n): ")
    if response and response[0] in 'yY':
        with open(jfile, 'w', encoding='utf-8') as j_file:
            json.dump(l, j_file)
    """

    helpers.add2json_file(d3, jfile)


# result lists
answers=dict(
true_true=["first\t Alex\n","",
"last", "Kleider","",
"payment","     200","",
"personID","     145"],

true_false=["personID","     145","",
"first", "     Alex","",
"last", "     Kleider", "",
"payment", "     200"],

false_true=['first: Alex','last: Kleider',
'payment: 200', 'personID: 145'],

false_false=["personID: 145", "first: Alex",
"last: Kleider", "payment: 200"],
)
#for key, value in answers.items():
#    print(key+": ",value)

def main():
    data = {}
    data['personID'] = 145
    data['first'] = "Alex"
    data['last'] = "Kleider"
    data['payment'] = 200
    print("-----------true/true")
    print(helpers.show_dict(data,
                    extra_line=True,
                    ordered=True))
    print()
    print("-----------true/false")
    print(helpers.show_dict(data,
                    extra_line=True,
                    ordered=False))
    print()
    print("----------false/true")
    print(helpers.show_dict(data,
                    extra_line=False,
                    ordered=True))
    print()
    print("----------false/false")
    print(helpers.show_dict(data,
                    extra_line=False,
                    ordered=False))
    print()

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
#   main()

