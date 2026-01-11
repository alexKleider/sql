#!/usr/bin/env python3

# File: oldtimers.py

"""
Provides an ordered listing of when current
members joined ordered by longest first.

see: Sql/oldtimersFF.sql
"""

from code import routines
from code import helpers

n2display = 25
yr_later = helpers.add_yr(helpers.eightdigitdate)
seniors_file = "seniors.csv"

def old_timers(n2display=n2display):

    query = f"""
    /* File: Sql/oldtimersFF.sql */

    /* Provides an ordered listing of when current
       members joined ordered by longest first.  */

    -- requires fomatting: a date 1yr later than current date
    -- and set LIMIT on how many you want to be listed

    SELECT P.first, P.last, S.begin 
    FROM People as P
    JOIN Person_Status as S
    WHERE S.begin != '' AND (S.end >"{yr_later}" OR end = "")
    AND P.personID = S.personID
    ORDER BY S.begin
    LIMIT {n2display};
    """

    listing = routines.fetch(query, from_file=False)
    return listing

if __name__ == "__main__":
    seniors = old_timers()
    for item in seniors:
        print(item)
    yn = input("Send data to a csv file?.(y/n) ")
    if yn and yn[0] in "yY":
        helpers.dump2csv_file(seniors,
                              keys=("first", "last", "joined"),
                              file_name=seniors_file)

