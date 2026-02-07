#!/usr/bin/env python3

# File: dues.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

from code import routines

query = """SELECT P.last, P.first, P.suffix,
                D.dues_owed
            FROM Dues as D
            JOIN People as P
            ON P.personID = D.personID
            WHERE D.dues_owed != 0
            ;"""

keys = routines.query_keys(query)

res = routines.fetch(query, from_file=False)
for line in res:
    print(line)
routines.query2csv(query, "dues.csv")

