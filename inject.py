#!/usr/bin/env python3

# File: inject.py

import sys
import sqlite3
from code import routines

noneed = """
query_file = 'Sql/inject_date.sql'
with open(query_file, 'r') as infile:
    query_from_file = infile.read()
"""

setApplicant = """
UPDATE Applicants
SET {} = ?
WHERE personID = ?
;
"""

setPeople = """
UPDATE People
SET {} = ?
WHERE personID = ?
"""

query = setPeople.format('state')
params = ('NJ', 198, )
print(query, params)
#sys.exit()

routines.fetch(query, from_file=False,
        params=params,
        commit=True)

