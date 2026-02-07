#!/usr/bin/env python3

# File: data_entry.py

"""
GUI prompt for demographics.
A dict is returned.
"""

from Kinter import collector
from code import routines

def data_entry(table="People",
               header="Enter New Person Demographics",
               skipID=False):  # skips record[0] (ID)
    """ Returns data to populate specified table """
    query = f"PRAGMA table_info({table});"
    _ = input(f"{query=}")
    res = routines.fetch(query,
                         from_file=False)
    _ = input(f"{res=}")
    if skipID:
        keys = [item[1] for item in res][1:]
    else: keys=  [item[1] for item in res]
    map0 = {}
    for key in keys:
        map0[key] = ""
    return collector.updated_mapping(map0,
                    "Enter New Person Demographics")

if __name__ == "__main__":
    mapping = data_entry(table="Applicants",
                         header="Enter Applicant Details",
                         skipID=False)
    if mapping:
        print("Returning following mapping:")
        for key, value in mapping.items():
            print(f"    {key}: {value}")
    else:
        print("<data_entry> returned empty.")
