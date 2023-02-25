#!/usr/bin/env python3

# File: test_query.py

"""
Takes one parameter: an sql query file.
Returns the result of the query.
"""

import sys
import sqlite3
from code import routines


if not len(sys.argv) > 1:
    print("Must provide an sql query file as a parameter.")
    sys.exit()
else:
    query_file = sys.argv[1]
if len(sys.argv) > 2:
    format = sys.argv[2]

ret = routines.get_query(query_file)
print(ret)

ret = routines.get_query_result(query_file, params=('z5_d_odd',))
for line in ret:
    print(line)


