#!/usr/bin/env python3

# File: mv_cost2owing.py

"""
One time use after added owing field to Moorings table.
Ed and Don had already paid so their cost needs to be re-entered.
"""

from code import routines

query = "SELECT * FROM Moorings;"
response = routines.fetch(query, from_file=False)
for line in response:
    print(line)
    query = f"UPDATE Moorings SET owing = {line[2]} WHERE mooringID = {line[0]};"
#   print(query)
    routines.fetch(query, from_file=False, commit=True)

