#!/usr/bin/env python3

# File: add2json.py

"""
Testing code.helpers.add2json_file()
"""

import json
#import sys
#import os
#sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import helpers

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


