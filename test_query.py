#!/usr/bin/env python3

# File: test_query.py

"""
Takes one optional parameter: an sql query file.
Returns the result of the query.
If a file name is not provided, must hard code it.
"""

import sys
import sqlite3
from code import routines


if not len(sys.argv) > 1:
    query = """
        SELECT personID, first, last, suffix
    FROM People
    WHERE first LIKE ? OR last LIKE ?
    ;
    """
else:
    query_file = sys.argv[1]
    query = routines.get_query(query_file)
if len(sys.argv) > 2:
    params = sys.argv[2]

ret = routines.get_query_result(
        query,
#       db=db_file_name,  has a default set
        params= ('Al%', 'K%',),
        data=None,
        from_file=False,
        commit=False)

for line in ret:
    print(line)


