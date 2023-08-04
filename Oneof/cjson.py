#!/usr/bin/env python3

# File: cjson.py

"""
One time use to create a json file from 
an applicants application info.
"""

import os
import sys
import json
sys.path.insert(0, os.path.split(sys.path[0])[0])
from code import applicants

ap_info_file = "Secret/hmAp.txt"

with open(ap_info_file, 'r') as stream:
    source_data = [line for line in stream]
data = applicants.get_new_applicant_data(source_data)
for key, value in data.items():
    print(f"{key}: {value}")
with open ("ap_data.json", 'w') as stream:
    json.dump(data, stream)
    print(f"Data written to '{stream.name}'.")
