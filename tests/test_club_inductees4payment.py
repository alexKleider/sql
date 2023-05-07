#!/usr/bin/env python3

# File: tests/test_club_inductees4payment.py

import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
from code import club

holder = club.Holder()
club.assign_inductees4payment(holder)
for key, value in holder.working_data.items():
    print(f"personID/key is: {key}")
    for k, v in value.items():
        print(f"{k}: {v}")
#print(holder.working_daa)
