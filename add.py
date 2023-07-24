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


def get_keys_from_schema(table, nkeys2ignore=0):
    """
    query comes from: https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    <nkeys2ignore> provides ability to ignore any primary keys
    such as 'personID' (in which case it can be set to 1.
    """
    query =  f"pragma table_info({table})"
    res = routines.fetch(query, from_file=False)
    return  [item[1] for item in res[nkeys2ignore:]]
    # item[1] is the column/key.


def get_new_applicant_data(file_content, report=None):
    """
    <file_content> must refer to text read from a file having
    one line for each (except the first) field present in the
    'People' table schema followed by a line each for sponsor1,
    sponsor2, date application was received and date fee was
    received (enter '0' if fee did not accompany the application.
    Returns a dict with keys relevant to new applicants.
    Note: Sponsors in the source are by name (and may have a date
    after first and last names) but the returned dict has only
    "personID"s as sponsor entries.
    """
    data = [line for line in helpers.useful_lines(
                            file_content)]
    _ = input(f"data collected from file:\n{data}")
    keys = get_keys_from_schema('People', nkeys2ignore=1)
    keys.extend(
        ['sponsor1ID', 'sponsor2ID', 'app_rcvd', 'fee_rcvd'])
    _ = input(f"keys collected from file:\n{keys}")
#   print(data)
#   print(keys)
    ret = dict(zip(keys, data))
    _ = input(f"Resulting dict:\n{ret}")
    if ret['suffix'] == 'No Suffix': ret['suffix'] = ''
    if ret['app_rcvd'] == 0: ret['app_rcvd'] = ''
    if ret['fee_rcvd'] == 0: ret['fee_rcvd'] = ''
    with open("Sql/id_from_names_ff.sql", 'r') as inf:
        query = inf.read()
    for sponsor in ('sponsor1ID', 'sponsor2ID'):
        first, last, date = ret[sponsor].split()
        res = routines.fetch(query.format(first, last),
                            from_file=False)
        ret[sponsor] = res[0][0]
#       _ = input(ret[sponsor])
    if isinstance(report, list):
        report.append(
            f"get_new_applicant_data() called on\n{file_content}")
        if (not (len(data) == len(keys))):
            report.append("Lengths don't match.")
        report.append(f"get_new_applicant_data returning:\n{ret}")
    return ret  # returns dict of new applicant data from file


def add_new_applicant_cmd():
    """
    """
    ret = ["Entering add_new_applicant_cmd...",]
    print(ret[0])
    ret.append("  == currently under development ==")
    while True:
        answer = input(
                "CLInput or from file? (c,C,f,F,q)uit): ")
        if answer and answer[0] in "qQ":
            ret.append("Aborting addition of new applicant(s)!")
            return ret
        if answer[0] in "fF":
            fname = input("File name: ")
            ret.append(f"Getting data from {fname}...")
            stream = []
            try:
                with open(fname, 'r') as inf:
                    for line in inf:
                        stream.append(line)
            except FileNotFoundError:
                ret.append("File not found, try again.")
                print(ret[-1])
                continue
            data = get_new_applicant_data(stream, report=ret)
            break
    _ = input(f"So far following has been collected:\n{data}")
    return ret


def test_add_new_applicant_cmd():
    for line in add_new_applicant_cmd():
        print(line)


def test_all_schema():
    for schema in ("People", "Person_Status", "Stati",
            "Attrition", "Applicants", "Receipts", "Dues",
            "Moorings", "Dock_Privileges", "Kayak_Slots" ):
        print(get_keys_from_schema(schema, 0))


def test_applicant_data_collection():
    with open('Secret/Applicants/hmAp.txt', 'r') as stream:
        a_content = [line for line in stream]
    a = get_new_applicant_data(a_content)
    with open('Secret/Applicants/wjAp.txt', 'r') as stream:
        b_content = [line for line in stream]
    b = get_new_applicant_data(b_content)
    for res in (a, b):
        for key, value in res.items():
            print(f"{key}: {value}")
        print()


if __name__ == '__main__':
#   test_add_new_applicant_cmd()
#   test_applicant_data_collection()
    test_all_schema()

