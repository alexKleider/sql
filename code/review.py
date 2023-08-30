#!/usr/bin/env python3

# File: code/review.py

"""
Code involved in reviewing data that is time sensitive.
Main item is when a new member (a year later) becomes
a member in good standing.
"""

import csv
import helpers
import routines

# first let's look at all the applicants...
applicants_csv = "Secret/applicants.csv"
non_m_non_o_stati_csv = "Secret/non_member_officer.csv"

def applicants2csv():
    """
    See what's in our applicants table.
    """
    keys = routines.get_keys_from_schema("Applicants")
    query = """SELECT * FROM Applicants
    ;"""
    res = routines.fetch(query, from_file=False)
    print(f"Writing data to {applicants_csv}")
    with open(applicants_csv, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=keys)
        writer.writeheader()
        for entry in res:
            writer.writerow(helpers.make_dict(keys, entry))

def non_member_non_officer_stati2csv():
    """
    """
    keys = routines.get_keys_from_schema("Person_Status")
    query = """Select * FROM Person_Status
            WHERE NOT statusID in (15, 20, 21, 22, 23, 24, 25)
            ;"""
    res = routines.fetch(query, from_file=False)
    print(f"Writing data to {non_m_non_o_stati_csv}")
    with open(non_m_non_o_stati_csv, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=keys)
        writer.writeheader()
        for entry in res:
            writer.writerow(helpers.make_dict(keys, entry))
    pass


if __name__ == '__main__':
    applicants2csv()
    non_member_non_officer_stati2csv()
