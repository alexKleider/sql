#!/usr/bin/env python3

# File: try.py

import sys
import sqlite3
from code import routines

query_file = 'Sql/inject_date.sql'
with open(query_file, 'r') as infile:
    query_from_file = infile.read()

query = """
UPDATE Applicants
SET {} = ?
WHERE personID = ?
;
"""

query = query.format('approved')
query_from_file = query_from_file.format('approved')
print(query)
print(query_from_file)
#sys.exit()

routines.fetch(query_from_file, from_file=False,
        params=('230301', 119,),
        commit=True)

