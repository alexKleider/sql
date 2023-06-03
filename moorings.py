#!/usr/bin/env python3

# File: moorings.py

"""
Reads the sql db and returns info regarding moorings.
Should probably eventually be ammalgamated into code.commands.py.
"""

import csv
from code import routines

keys = "mooringID, mooring_code, mooring_cost, personID, owing"
query = "SELECT {} FROM Moorings;".format(keys)

def get_name(personID):
    if not personID:
        return ""
    name_query = """SELECT first, last, suffix
            FROM People
            WHERE personID = ?;"""
    res = routines.fetch(name_query, 'Secret/club.db',
            from_file=False, params=[personID, ])[0]
    suffix = res[2]
    if suffix:
        suffix = f" {suffix}"
    return "{0:} {1:}".format(*res) + suffix


q_res = routines.fetch(query, 'Secret/club.db',
            from_file=False)
fieldnames = ("mooring_ID", "code", "cost", "name", "owing")
res = []
for line in q_res:
    print(line)
    res.append({
        fieldnames[0]: line[0],
        fieldnames[1]: line[1],
        fieldnames[2]: line[2],
        fieldnames[3]: get_name(line[3]),
        fieldnames[4]: line[4],
        })
for entry in res:
    print([value for value in entry.values()])
response = input(
        "\nCreate a csv file ? (enter name or leave blank).. ")
if response:
    with open(response, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in res:
            writer.writerow(rec)

