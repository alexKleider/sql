#!/usr/bin/env python3

# File: code/attrition.py

import helpers
import routines

while True:
    begin = input("Attrition since date (YYYYMMDD): ")
    if not begin:
        index = 0
        break
    if len(begin) == 8 and begin.isdigit():
        index = 1
        break

queries = (
"""SELECT P.personID, P.first, P.last, P.suffix, P.email, 
            PS.begin, PS.statusID
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 27, 28)
                AND (PS.end = '' OR PS.end > {})
                AND (PS.begin < {})
            ORDER BY P.last
            ; """.format(helpers.eightdigitdate,
                        helpers.eightdigitdate),

"""SELECT P.personID, P.first, P.last, P.suffix, P.email,
            PS.begin, PS.statusID
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 27, 28)
                AND PS.begin >= {}
                AND (PS.end = '' OR PS.end > {})
                AND (NOT PS.begin > {})
            ORDER BY P.last
            ; """.format(begin,
                    helpers.eightdigitdate,
                    helpers.eightdigitdate),
            )
query = queries[index]

def select(item):
    l = item.split()
    return l[1]

res = routines.fetch(query, from_file=False)
ret = []
for entry in res:
    l = list(entry)
    l[-1] = str(l[-1])
    l[0] = str(l[0])
    ret.append(' '.join(l))

print(f"n = {len(ret)}, begin set to {begin}, using query {index}")
for entry in sorted(set(ret),key=select):
    print(entry)
