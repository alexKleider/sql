#!/usr/bin/env python3

# File receipts.py

"""
Call using the following syntax:
$ python -m utils.receipts
or
use the first section...
See  File: ~/Notes/Py/cwd.py
"""
import os
import sys
cwd = os.getcwd()
# print(f"sys.path is {sys.path}")
if not cwd in sys.path:
    sys.path.insert(0, cwd)
# print(f"sys.path is now {sys.path}")

from code import routines
from code import helpers

today = helpers.eightdigitdate

query = """SELECT P.personID, P.first, P.last, R.date_received,
            R.acknowledged, R.dues, R.ap_fee FROM People as P
            JOIN Receipts as R
            ON P.personID = R.personID
            WHERE R.date_received > "20250000"
            ORDER BY R.date_received
        ;"""

if __name__ == "__main__":
    outfile = f"receipts{today}.csv"
    routines.query2csv(query, outfile)
    print(f"Output sent to '{outfile}'")

