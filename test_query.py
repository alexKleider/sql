#!/usr/bin/env python3

# File: test_query.py

"""
Takes one parameter: an sql query file.
Returns the result of the query.
"""

import sys
from code import commands


if not len(sys.argv) > 1:
    print("Must provide an sql query file as a parameter.")
    sys.exit()
else:
    query_file = sys.argv[1]

for item in commands.fetch(query_file):
    print(item)

