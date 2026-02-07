#!/usr/bin/env python3

# File: members_.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

from code import routines
from code import helpers

today = helpers.eightdigitdate

query = f"""SELECT * FROM People as P
            JOIN Person_Status as S
            ON S.personID = P.personID
            WHERE S.statusID in (11, 15)
                AND ((S.begin <= {today} OR S.begin = "")
                    AND (S.end >={today} or S.end = ""))
            ORDER BY P.last, P.first
            ;"""

keys = routines.query_keys(query)

res = routines.fetch(query, from_file=False)
for line in res:
    print(line)
routines.query2csv(query, "members_.csv")

