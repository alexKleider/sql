#!/usr/bin/env python3

# File: add.py

import sys
from code import routines
from code import helpers

"""
Temporary file for development of code to deal with applicants:
- register new applicant(s)
- enter each meeting when it occurs.
- deal with "expired" application when appropriate.
- possibly deal with making applicant into a member.
- possibly move member from 1st year member to member in good
standing.
"""


def get_keys_from_schema(table):
    """
    query comes from: https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    """
    query =  f"pragma table_info({table})"
    res = routines.fetch(query, from_file=False)
#   print(res)
    return([item[1] for item in res[1:]]) # exclude personID key


def get_new_applicant_data(fname, ret=None):
    """
    <fname> must have one line for each (except the first) field
    present in the 'People' table schema followed by a line each
    for sponsor1, sponsor2, date application was received and
    date fee was received (enter '0' if fee did not accompany
    the application.)
    """
    with open(fname, 'r') as stream:
        data = [line for line in helpers.useful_lines(stream)]
    keys = get_keys_from_schema('People')
    keys.extend(
        ['sponsor1ID', 'sponsor2ID', 'app_rcvd', 'fee_rcvd'])
#   print(data)
#   print(keys)
    if isinstance(ret, list):
        ret.append(f"get_new_applicant_data({fname}) called")
        if (not (len(data) == len(keys))):
            ret.append("Lengths don't match.")
    ret = (dict(zip(keys, data)))
    if ret['suffix'] == 'No Suffix': ret['suffix'] = ''
    return ret


def add_new_applicant_cmd():
    """
    """
    ret = ["Entering add_new_applicant_cmd...",]
    print(ret[0])
    keys = get_keys_from_schema('People')
    ret.append("  == currently under development ==")
    while True:
        source = input(
                "CLInput or from file? (c,C,f,F,q)uit): ")
        if source and source[0] in "qQ":
            ret.append("Aborting addition of new applicant(s)!")
            return ret
        if source[0] in "fF":
            fname = input("File name: ")
            try:
                with open(fname, r) as inf:
                    data = inf.read()
            except FileNotFoundError:
                print("Invalid file name, try again.")
                continue
            data = data.split('\n')
            valid_data = []
            for line in data:
                line = line.strip()
                if line.startswith("#"):
                    continue
                valid_data.append(line)
            if len(valid_data) != len(keys):
                print(f"{fname} has wrong number of lines")
                continue
            pass
    return ret

if __name__ == '__main__':
#   add_new_applicant_cmd()
#   print(get_keys_from_schema('People'))
    a = get_new_applicant_data('Secret/Applicants/hmAp.txt')
    b = get_new_applicant_data('Secret/Applicants/wjAp.txt')
    for res in (a, b):
        for key, value in res.items():
            print(f"{key}: {value}")
        print()

