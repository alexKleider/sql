#!/usr/bin/env python3

# File: code/collect.py

"""
A place for routines that collect data.
Much from other modules should be moved here.
"""



try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

n2display = 25
yr_later = helpers.add_yr(helpers.eightdigitdate)
seniors_file = "seniors.csv"

def old_timers(n2display=n2display):
    """
    Provides a listing of dicts showing
        personID, first, last and date joined data  # [1]
    for members ordered by time as members.
    Note: if changing the keys, must make the modification
    in three places!!!  See [n] comments.
    see: Sql/oldtimersFF.sql
    """
    query = f"""
    SELECT P.personID, P.first, P.last, S.begin  -- [2]
    FROM People as P
    JOIN Person_Status as S
    WHERE S.begin != '' AND (S.end >"{yr_later}" OR end = "")
    AND P.personID = S.personID
    ORDER BY S.begin
    LIMIT {n2display};
    """
    listing = routines.fetch(query, from_file=False)
    keys = "personID", "First", "Last", "Date Joined"  # [3]
    return [dict(zip(keys, values)) for values in listing]

def ck_oldtimers():
    seniors = old_timers()
    keys = "personID", "First", "Last", "Date Joined"  # [3]
    for item in seniors:
        print(f"{item[keys[0]]}, {item[keys[1]]}, {item[keys[2]]},  {item[keys[1]]}")
#   yn = input("Send data to a csv file?.(y/n) ")
#   if yn and yn[0] in "yY":
#       helpers.dump2csv_file(seniors,
#                             keys=("first", "last", "joined"),
#                             file_name=seniors_file)

if __name__ == "__main__":
    print("entering collect module")
    ck_oldtimers()


    pass
