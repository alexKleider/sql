#!/usr/bin/env python3

# File: add.py

import sys
import json
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
#   _ = input(f"data collected from file:\n{data}")
    keys = get_keys_from_schema('People', nkeys2ignore=1)
    keys.extend(
        ['sponsor1ID', 'sponsor2ID', 'app_rcvd', 'fee_rcvd'])
#   _ = input(f"keys collected from file:\n{keys}")
    ret = dict(zip(keys, data))
#   _ = input(f"Resulting dict:\n{ret}")
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


def populate_db(data):
    """
    <data> is a dict created based on an application.
    Entries need to be made into the following tables:
    People: demographics
    Person_Status: 1. no fee, 2. fee paid, (3. acknowledged (a0))
    Applicants: sponsor1ID, sponsor2ID, app_rcvd, fee_rcvd
    """
    # data for People table is standard demographics
    #   ... already collected but need assigned personID
    # data for Person_Status table:
    all_keys = [key for key in data.keys()]
    key_params = ', '.join(all_keys[:10])
    all_values =  [value for value in data.values()]
    val_params = '"' + '", "'.join(all_values[:10]) + '"'
    insert_query = f"""
    INSERT INTO People ({key_params})
    VALUES ({val_params})
    ;"""
#   print(insert_query)
    res = routines.fetch(insert_query,
            from_file=False,
            commit=True)
    # Need to retrieve newly assigned personID...
    with open("Sql/id_from_names_fff.sql", 'r') as stream:
        getIDquery = stream.read()
    getIDquery = getIDquery.format(**data)
    res = routines.fetch(getIDquery,
            from_file=False)
    data['personID'] = res[0][0]
#   _ = input(f"personID is {data['personID']}")

    # Set data needed for Person_Status entry...
    #  /* Sql/person_status_entry_fd.sql */
    if data["fee_rcvd"]: data['statusID'] = 2
    else: data['statusID'] = 1  # Will have to add an end date
                        # and make another status entry
                        # when fee is paid.
    data["begin"] = helpers.sixdigitdate
    # Finally create entry in Applicants table...
    #  /* Sql/applicant_entry_d.sql */
    print()
    for key, value in data.items():
        print(f"{key}: {value}")
     


def test_populate_db():
    with open("ap_data.json", 'r') as source:
        data = json.load(source)
    populate_db(data)


def add_new_applicant_cmd():
    """
    Plan to have two input methods:
    1. from a specially formatted file (already implemented,) or
    2. item by item entry as prompted from the command line.
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
        elif answer[0] in "cC":
            print(
              "Command line prompted input not yet implemented.")
            _ = input("   CR to continue... ")
    print(f"\nSo far following has been collected:\n{data}")
    yn = input("OK to made data base entries? (y/n) ")
    if yn and yn[0] in "yY":
        populate_db(data)
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
    test_populate_db()
#   test_add_new_applicant_cmd()
#   test_applicant_data_collection()
#   test_all_schema()

