#!/usr/bin/env python3

# File: dock.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

from code import routines

query = """SELECT P.last, P.first, P.suffix,
                D.cost
            FROM People as P
            JOIN Dock_Privileges as D
            ON P.personID = D.personID
            ;"""

keys = routines.query_keys(query)

res = routines.fetch(query, from_file=False)
for line in res:
    print(line)
routines.query2csv(query, "dock.csv")

