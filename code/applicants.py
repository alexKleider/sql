#!/usr/bin/env python3

# File: applicants.py

import sys
import json

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

"""
File for development of code to deal with applicants:
- register new applicant(s)
- enter each meeting when it occurs.
- deal with "expired" application when appropriate.
- possibly deal with making applicant into a member.
- possibly move member from 1st year member to member in good
standing.
"""


def get_new_applicant_data(file_content, report=None):
    """
    <file_content> must refer to text read from a file having
    one line for each (except the first) field present in the
    'People' table schema followed by a line each for sponsor1,
    sponsor2, date application was received and date fee was
    received (enter '0' if fee did not accompany the application.
    Returns a dict with keys relevant to new applicants.
    Note: Sponsors in the source are by three names (first, last,
    suffix) and a date (which is not used)
    but the code translates these into personID numbers.
    """
    data = [line for line in helpers.useful_lines(
                            file_content)]
#   _ = input(f"data collected from file:\n{data}")
    keys = routines.get_keys_from_schema(
                            'People', nkeys2ignore=1)
    keys.extend(
        ['sponsor1ID', 'sponsor2ID', 'app_rcvd', 'fee_rcvd'])
#   _ = input(f"keys collected from file:\n{keys}")
    ret = dict(zip(keys, data))
#   _ = input(f"Resulting dict:\n{ret}")
    if ret['suffix'] == 'No Suffix': ret['suffix'] = ''
    if ret['app_rcvd'] == 0: ret['app_rcvd'] = ''
    if ret['fee_rcvd'] == 0: ret['fee_rcvd'] = ''
    with open("Sql/id_from_names_fd.sql", 'r') as inf:
        query = inf.read()
    for sponsor in ('sponsor1ID', 'sponsor2ID'):
        tup = ret[sponsor].split()
        l = len(tup)
        d = {"first": tup[0], "last": tup[1], "suffix": ''}
        if l == 4:
            d["suffix"] = tup[2]
        res = routines.fetch_d_query(
                "Sql/id_from_names_fd.sql", data=d)
#       _ = input(f"fetch_d_query on {d} returning {res}")
        ret[sponsor] = res[0][0]
    if isinstance(report, list):
#       report.append(
#           f"get_new_applicant_data() called on\n{file_content}")
        if (not (len(data) == len(keys))):
            report.append("Lengths don't match.")
        report.append(f"get_new_applicant_data returning:\n{ret}")
    return ret  # returns dict of new applicant data from file


def add2AppTable(data, record=None):
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
    res = routines.fetch_d_query("Sql/id_from_names_fd.sql",
            data)
    data['personID'] = res[0][0]
#   _ = input(f"personID is {data['personID']}")

    # Set data needed and then make the Person_Status entry...
    if data["fee_rcvd"]: data['statusID'] = 2
    else: data['statusID'] = 1  # Will have to add an end date
                        # and make another status entry
                        # when fee is paid.
    data["begin"] = helpers.eightdigitdate
    _ = routines.fetch_d_query(
            "Sql/person_status_entry_fd.sql", data, commit=True)
    # Finally create entry in Applicants table...
    _ = routines.fetch_d_query(
            "Sql/applicant_entry_fd.sql", data, commit=True)
    if record and isinstance(record, list):
        record.extend((
            "{first} {last} {suffix} added as new applicant."
                .format(**data),
            "Tables updated: People, Person_Status & Applicants.",
            "Still need to mail welcome letter.",
            ))


def test_add2AppTable():
    with open("ap_data.json", 'r') as source:
        data = json.load(source)
    add2AppTable(data)


def add_new_applicant_cmd():
    """
    Plan to have two input methods:
    1. from a specially formatted file (already implemented,) or
    2. item by item entry as prompted from the command line.
    """
    ret = ["Entering add_new_applicant_cmd...",]
    print(ret[0])
    ret.append("  == currently under development ==")
    # 1st choose method of input- only by file implemented 4 now
    # and collect the data...
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
            # get the data taken from application and transcribed
            # into a text file one line per data item:
            data = get_new_applicant_data(stream, report=ret)
            break
        elif answer[0] in "cC":
            print(
              "Command line prompted input not yet implemented.")
            _ = input("   CR to continue... ")
    print(f"\nSo far following has been collected:\n{data}")
    yn = input("OK to made data base entries? (y/n) ")
    if yn and yn[0] in "yY":
        add2AppTable(data)  # adds to three tables:
            #1. People
            #2. Person_Status
            #3. Applicants
    return ret


def credit_applicant_meeting_cmd():
    ret = ["Registering applicant's meeting attendance.", ]
    pass
    return ret


def applicant_data_entry_cmd():
    """
    """

    main_menu = {
        "Add new applicant": add_new_applicant_cmd,
        }
    ret = ['Entering applicant data entry...',]
    print(ret[0])
    ret.extend(helpers.choose_and_run(main_menu))
    return ret


def test_add_new_applicant_cmd():
    for line in add_new_applicant_cmd():
        print(line)


def test_all_schema():
    for schema in ("People", "Person_Status", "Stati",
            "Attrition", "Applicants", "Receipts", "Dues",
            "Moorings", "Dock_Privileges", "Kayak_Slots" ):
        print(routines.get_keys_from_schema(schema, 0))


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
#   test_add2AppTable()
    test_add_new_applicant_cmd()
#   test_applicant_data_collection()
#   test_all_schema()

