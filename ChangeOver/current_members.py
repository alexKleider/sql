#!/usr/bin/env python3

# File: current_members.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

from code import helpers
from code import routines
today = helpers.eightdigitdate

query = f"""SELECT last, first, suffix, phone, email,
                address, town, state, postal_code
        FROM People AS P
        JOIN Person_Status AS S
        ON P.personID = S.personID
        WHERE S.statusID in (11, 15)
            AND (
                (S.begin <= {today} OR S.begin = "")
                AND
                (S.end >= {today} or S.end = "")
            )
        ORDER BY P.last, P.first
        ; """

routines.query2csv(query, "current_members.csv")
#res = routines.fetch(query, from_file=False)
#for entry in res:
#    print(entry)
