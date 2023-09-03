#!/usr/bin/env python3

# File: code/attrition.py

import helpers
import routines

query = """SELECT P.first, P.last, P.suffix, P.email
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 27, 28)
                AND (PS.end = '' OR PS.end > {})
            ORDER BY P.last
            ; """.format(helpers.eightdigitdate)

def select(item):
    l = item.split()
    return l[1]

res = routines.fetch(query, from_file=False)
ret = []
for entry in res:
    ret.append(' '.join(entry))
for entry in sorted(set(ret),key=select):
    print(entry)
