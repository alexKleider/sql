#!/usr/bin/env python3

# File: inject.py

"""
Currently this is my method to inject data into the data base.
It requires modification of the code in this file for each task!!
"""

import sys
import sqlite3
from code import routines

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

setState = """
UPDATE People
SET state = ?
WHERE personID = ?
"""

query = setPeople.format('state')
params = ('CA', 73, )
print(query, params)
#sys.exit()
listing = (
        ('UT', 38, ),
        ('CA', 73, ),
        ('CA', 112, ),
        )

for params in listing:
    routines.fetch(setState, from_file=False,
        params=params,
        commit=True)

