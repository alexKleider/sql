#!/usr/bin/env python3

# File: code/data_entry.py

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

try: from code import textual
except ImportError: import textual

"""
Handle adding data to the db.
An ammalgamation of what used to be applicants.py
and update.py

Provides
    data_entry.add_new_applicant_cmd()
    data_entry.change_status_cmd() (under development)
    data_entry.applicant_update_cmd() (under development)
"""

def add2tables(data, report=None):
    """
    One time use for each new applicant.
    <data> is a dict created based on an application.
    Entries need to be made into the following tables:
    People: demographics
    Person_Status: 1. no fee, 2. fee paid, (3. acknowledged (a0))
    Applicants: sponsor1ID, sponsor2ID, app_rcvd, fee_rcvd
    ## Missing is an entry into the Receipts table
    """
    # data for People table is standard demographics
    #   ... already collected but need assigned personID
    # data for Person_Status table:
    all_keys = [key for key in data.keys()]
    key_params = ', '.join(all_keys[:10])
    all_values =  [value for value in data.values()]
    # all values to be entered into People table are text:
    val_params = '"' + '", "'.join(all_values[:10]) + '"'
    people_insert_query = f"""
    INSERT INTO People ({key_params})
    VALUES ({val_params})
    ;"""
    print('\n' + people_insert_query)
    yn = input(
        f"OK to commit the query shown above?: (y/n): ")
    if yn and yn[0] in 'Yy':
        res = routines.fetch(people_insert_query,
                from_file=False,
                commit=True)
        print("...successfull addition to People table.")
        # Need to retrieve newly assigned personID...
        res = routines.fetch_d_query("Sql/id_from_names_fd.sql",
                data)
        data['personID'] = res[0][0]
        print(f"New personID is {data['personID']}")
    else: 
        _ = input("Aborting data entry! rtn to continue: ")
        return

    # Set data needed and then make the Person_Status entry...
    if data["fee_rcvd"]:
        ## good place to make entry into Receipts table ##
        # .. use data['personID']
        data['statusID'] = 2
        data['begin'] = data['fee_rcvd']
    else:
        data['statusID'] = 1  # Will have to add an end date
                        # and make another status entry
                        # when fee is paid.
        data['begin'] = data['app_rcvd']
    _ = routines.fetch_d_query(
            "Sql/person_status_entry_fd.sql", data, commit=True)
    # Finally create entry in Applicants table...
    _ = routines.fetch_d_query(
            "Sql/applicant_entry_fd.sql", data, commit=True)
    if report and isinstance(report, list):
        report.extend((
            "{first} {last} {suffix} added as new applicant."
                .format(**data),
            "Tables updated: People, Person_Status & Applicants.",
            "Still need to mail welcome letter.",
            "Also: need to make an entry into Receipts table prn",
            ))


def file2app_data(file_content, report=None):
    """
    Returns a dict with keys relevant to new applicants.
    <file_content> must refer to text read from a file having
    one line for each (except the first) field present in the
    'People' table schema followed by a line each for sponsor1,
    sponsor2, date application was received and date fee was
    received (enter '0' if fee did not accompany the application.
    Note: Sponsors in the source are by three names (first, last,
    suffix) and a date (which is not used)
    but the code translates these into personID numbers.
    """
    data = [line for line in helpers.useful_lines(
                            file_content)]
#   _ = input(f"data collected from file:\n{data}")
    keys = routines.keys_from_schema(
                    'People', brackets=(1,0))
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
#           f"file2app_data() called on\n{file_content}")
        if (not (len(data) == len(keys))):
            report.append("Lengths don't match.")
        report.append(f"file2app_data returning:\n{ret}")
    return ret  # returns dict of new applicant data from file


def add_new_applicant_cmd():
    """
    Provides ability to enter one new applicant into the db:
    Creats appropriage entries in "People", "Person_Status"
    and "Applicant" tables. 
    Returns a report (in the form of a list of lines.)
    Two input methods:
    1. from a specially formatted file    or
    2. item by item entry as prompted from the command line.
        - the latter is under development: code/textual.py
    """
    ret = ["Entering add_new_applicant_cmd...",]
    print(ret[0])
    ret.append(
        "  == so far data entry from file implemented  ==")
    # 1st choose method of input- only by file implemented 4 now
    # and collect the data...
    while True:  # get data (/w option to file ==> db) OR abort
        answer = input(
                "CLInput or from file? (c,C,f,F,q)uit): ")
        if answer and answer[0] in "qQ":
            # option to abort without adding data
            ret.append("Aborting addition of new applicant(s)!")
            return ret
        if answer[0] in "fF":
            fname = input("File name: ")
            ret.append(f"Getting data from {fname}...")
            stream = []
            try:
                with open(fname, 'r') as inf:
                    for line in helpers.useful_lines(inf):
                        stream.append(line)
            except FileNotFoundError:
                ret.append("File not found, try again.")
                print(ret[-1])
                continue
            # get the data taken from application and transcribed
            # into a text file one line per data item:
            data = file2app_data(stream, report=ret)
            break
        elif answer[0] in "cC":
            data = textual.get_demographics(report=ret)
            if data:
                break
    routines.add_sponsorIDs(data)
    print(f"\nSo far following has been collected:\n{data}")
    yn = input("OK to make data base entries? (y/n) ")
    if yn and yn[0] in "yY":
        add2tables(data, report=ret)  # adds to three tables:
            #1. People
            #2. Person_Status
            #3. Applicants
    return ret

def change_status_cmd(report=None):
    routines.add2report(report, 
            "Entering code/data_entry/change_status_cmd...")
    data = textual.selectP_record(report=report)
    if not data:
        routines.add2report(report,
            "code/data_entry/selectP_record " +
            "failed to return a record")
        return
    else:
        routines.add2report(report,
            "<data> now contains a People table entry")
    personID = data['personID']
    fields = ('personID', 'statusID', 'begin', 'end', )[1:]
    e,v = textual.get_mode(data, fields)
    rep = ["textual.get_mode(data,fields) returning ...",]
    rep.append(f"e:{repr(e)}")
    for key, value in v:
        rep.append(f"{key}: {value}")
    for line in rep:
        report.append(line)
        print(line)
    routines.add2report(report,
        "...finished code/data_entry/change_status.cmd.")


def applicant_update_cmd():
    """
    """
    report = ["Entering applicant_update_cmd...", ]
    report.extend(["under development....",
            "Leaving applicant_update_cmd",])
    return report


def test_add_new_applicant_cmd():
    for line in add_new_applicant_cmd():
        print(line)

if __name__ == "__main__":
    test_add_new_applicant_cmd()
