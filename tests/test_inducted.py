#!/usr/bin/env python3

# File: tests/test_inducted.py

"""
Testing code.club.assign_inductees4payment(holder)
which requires Sql.inducted.sql
"""

import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import routines
from code import club

if __name__ == '__main__':
    holder = club.Holder()
    club.assign_inductees4payment(holder)
    for key, value in holder.working_data.items():
        if type(value) == dict:
            print(f"{key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"{key}: {value}")
