#!/usr/bin/env python3

# File: test_query.py

"""
Takes one parameter: an sql query file.
Returns the result of the query.
"""

import sys
import sqlite3


def get_query(sql_source_file, formatting=None):
    """
    Reads a query from a file.
    If <formatting> is provided: it must consist of either
    a sequence of length to match number of qmark placeholders
    or a dict containing all keys needed for named placeholders
    each of which is prefaced by a colon. eg: (:key1, :key2).
    """
    with open(sql_source_file, 'r') as source:
        ret = source.read()
        if formatting:
            ret = ret.format(*formatting)
        return ret


if not len(sys.argv) > 1:
    print("Must provide an sql query file as a parameter.")
    sys.exit()
else:
    query_file = sys.argv[1]

con = sqlite3.connect('Secret/club.db')
cur = con.cursor()

cur.execute(get_query(query_file))

while True:
#   print()
    res = cur.fetchone()
    if not res: break
    print(res)


