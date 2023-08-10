#!/usr/bin/env python3

# File: receipts.py

"""
Assumes existence of a 'receipts.csv' file.
Presents data sorted by last, first, suffix.
"""

import csv

def s(d):
    names = d['personID'].split()
    name = names[1:]
    name.append(names[0])
    return ''.join(name)

fieldnames = ("personID,date_received,dues,dock," +
          "kayak,mooring,acknowledged,ap_fee").split(',')
l = []
with open('receipts.csv', 'r', newline='') as inf:
    reader = csv.DictReader(inf)
    for d in reader:
        l.append(d)
l.sort(key=s)
print(fieldnames)
for d in l:
    print([value for value in d.values()])
