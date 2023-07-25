#!/usr/bin/env python3

# File: cjson.py

"""
One time use to create a json file from 
an applicants application info.
"""

import json
import add

ap_info_file = "ap.txt"

with open(ap_info_file, 'r') as stream:
    source_data = [line for line in stream]
data = add.get_new_applicant_data(source_data)
for key, value in data.items():
    print(f"{key}: {value}")
with open ("ap_data.json", 'w') as stream:
    json.dump(data, stream)
    print(f"Data written to '{stream.name}'.")
