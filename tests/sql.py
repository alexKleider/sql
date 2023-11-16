#!/usr/bin/env python3

# File: sql.py

"""
A place to test/develope queries.
"""

import csv
from code import routines

queries_w_keys = [
    ("""
        SELECT R.personID, P.first, P.last, P.suffix,
            R.date_received, R.dues, R.ap_fee
        FROM Receipts as R
        JOIN People as P
        ON P.personID = R.personID
        WHERE R.ap_fee != 0
        ORDER BY R.date_received;
    """,
    "personID first last suffix received dues ap_fee".split(),
    ),

    ("""
        SELECT 
--      WHERE R.date_received > "20230901"
    """,
    '',
    ),
        ]

def create_csv(res, keys=None, file_name="query.csv"):
    """
    Turn a query result (<res) into a csv file.
    If <keys> are provided (as an iterable) they will be
    written to the first line.
    """
#   print("begin running create_csv")
    with open(file_name, 'w', newline='') as outf:
        writer = csv.writer(outf)
#       print("Looking for keys to write..")
        if keys:
            writer.writerow(keys)
#       print("Looking for lines to write..")
        for line in res:
            writer.writerow(line)
#       print("Done with create_csv.")

def main(n):
    query, keys = queries_w_keys[n]
    if query.strip():
        res = routines.fetch(query, from_file=False)
        if keys:
            print(', '.join(keys))
        for line in res:
            print(repr(line))
        create_csv(res, keys=keys)

if __name__ == "__main__":
    n = int(input("which query? "))
    main(n)
