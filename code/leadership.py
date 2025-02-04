#!/usr/bin/env python3

# File: leadership.py

import helpers
import routines

today = helpers.eightdigitdate

query = f"""
    /* File: currentleadership.sql */

    SELECT P.personID, P.first, P.last, S.text, PS.begin, PS.end
    FROM People as P
    JOIN Person_Status as PS
    ON P.personID = PS.personID
    JOIN Stati as S
    ON S.statusID = PS.statusID
    WHERE S.statusID in (20, 21, 22, 23, 24, 25)
    AND PS.begin < {today}
    AND (PS.end = "" OR PS.end > {today})
    --ORDER BY P.last
    ORDER BY S.statusID
    ; """

res = routines.fetch(query, from_file=False)

for line in res:
    print(line)


