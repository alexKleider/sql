#!/usr/bin/env python3

# File: code/get_data_byID.py

import dates
import helpers

def get_data_byID(ID):
    return dates.get_demographic_dict(personID)

while True:
    personID = helpers.get_int(prompt="personID to query: ")
    if personID <= 0: break 
    data = get_data_byID(personID)
    if isinstance(data,dict):
        for key, value in data.items():
            print(f"{key}: {value}")
        print()
    else:
        print("No such personID.")
        print()
