#!/usr/bin/env python3

# File: kayak.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

from code import routines

query = """SELECT P.last, P.first, P.suffix,
                K.slot_code, K.slot_cost
            FROM People as P
            JOIN Kayak_Slots as K
            ON P.personID = K.personID
            ;"""

keys = routines.query_keys(query)

res = routines.fetch(query, from_file=False)
for line in res:
    print(line)
routines.query2csv(query, "kayak_data.csv")

