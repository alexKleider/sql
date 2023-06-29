#!/usr/bin/env python3

# File: code/remove_email.py

import csv
import club

source = club.EMAIL_JSON

if __name__ == '__main__':
    with open(source, newline='') as inf:
        reader = csv.DictReader(inf)
    print("so far so good")

