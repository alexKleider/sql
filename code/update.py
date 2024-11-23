#!/usr/bin/env python3

# File: code/update.py

"""
Probably superceeded by data_entry.py
See also ap_update for applicant status updates
Expect content of this file will incorporated elsewhere and
eventually redacted.
Might find quivalent code is now in code/data_entry.py

Prototyping a status_change_cmd
  add_status
    Add a status entry
  update_status
    Insert an "end" date (prn)
    & Add a status entry
See also ap_update.
"""

import helpers
import routines


doit = False  # when False only prints queries
              # when True runs queries

status_keys = routines.keys_from_schema("Stati")  # not used?
ps_keys = routines.keys_from_schema("Person_Status")

def status_choices():
    """    Possible stati (the Stati table)
    Returns a list of strings: Four header lines followed by
    all available stati with their statusID, code and text
    (to serve as a reference.)
    """
    res = routines.fetch("SELECT * FROM Stati;",
            from_file=False)
    ret = ["Stati from which to choose:",
           "===========================",
           "sID code         text",
           "--- ----         ----",
           ]
    for entry in res:
        ret.append("{0:>3} {1:<12} {2}".format(*entry))
    return ret

def status_entries4(personID):
    """
    Person_Status table entries pertenent to <personID>.
    Returned is a list (which may be empty) of dicts.
    """
    query = f"""
        SELECT * from Person_Status WHERE personID = {personID};
        """
    res = routines.fetch(query, from_file=False)
    ret = []
    for entry in res:
        ret.append(dict(zip(ps_keys, entry)))
    return ret

def quote_nonID_fields(data):
    """
    <data> is a dict/record
    the value of any non ID key is quoted.
    Works by side effect!
    Also returns the new dict.
    """
    for key, value in data.items():
        if not key.endswith("ID"):
            data[key] = f"'{value}'"
    return data


def get_stati(prompt=None, report=None):
    """
    If <prompt>: prints prompt.
    Calls routines.pick_People_record()
    Returns a dict of dicts based on entries in the
            Person_Status table for that personID.
    Returns None if no personID found.
    Returns the personID if no status entries found.
    The dict of dicts is to serve as a 'menu':
        1 based integer keys, dict for each value.
    """
    if isinstance(report, list):
        report.append("Entering update.setup(prompt)")
    if prompt:
        print(prompt)
    rec = routines.pick_People_record(header_prompt=(
        "Returning attempt at finding a person record"))
    if not rec:
        s = "record not found"
        if isinstance(report, list):
            report.append(s)
        _ = input(s)
        return
    else:
        personID = rec['personID']
#       print("Stati from which to choose:")
#       for line in status_choices():
#           print(f"  {line}")
        entries = status_entries4(rec["personID"])
        dicts = dict(zip(range(1, len(entries)+1), entries))
        if not dicts:  # no previous entries
            return personID
        return dicts

def update_status(report=None):
    """
    Update an existing entry.
    Returns a tuple: a personID and the query it uses
    OR the personID if there's no entry to update
    OR None if no personID found
    """
    prompt = "Running update_status()..."
    dicts = get_stati(prompt, report=report)
    if isinstance(dicts, int):
        report.append("No prior entries exist.")
        print(report[-1])
        report.append("No record to modify!")
        print(report[-1])
        return dicts  # returns personID if no stati exist
    print("What we have to work with:")
    for key, val in dicts.items():
        print(f"{key:>3}: {repr(val)}")
    while True:
        try:
            index = int(input("Which entry needs changed? "))
        except ValueError:
            print("Must enter an integer; try again!")
        else:
            break
    data = dicts[index]
    corrected = {}
    for key, value in data.items():
        if key == 'personID':
            corrected[key] = value
        else:
            corrected[key] = input(
                    f"  {key} was <{data[key]}> change to: ")
            if not key == 'statusID':
                corrected[key] = f"'{corrected[key]}'"
    _ = quote_nonID_fields(data)
    print(f"original version: {repr(data)}")
    _ = input(f"corrected version: {repr(corrected)}")
    f_new = ', '.join([f"{key} = {value}" for
                key, value in corrected.items()])
    f_original = ' AND '.join([f"{key} = {value}" for
                key, value in data.items()])
    query = f""" UPDATE Person_Status
            SET {f_new}
            WHERE {f_original}
            ; """
    _ = input(query)
#   routines.fetch(query, from_file=False, commit=True)
    return query

def change_status(report=None):
    """
    Change a person's status:
    i.e. end one status end begin another
    """
    prompt = "Running change_status()..."
    dicts = get_stati(prompt, report=report)
    if isinstance(dicts, int):
        report.append("No prior entries exist.")
        print(report[-1])
        report.append("No record to modify!")
        print(report[-1])
        return
    print("What we have to work with:")
    for key, val in dicts.items():
        print(f"{key:>3}: {repr(val)}")
    while True:
        try:
            index = int(input("Which entry needs changed? "))
        except ValueError:
            print("Must enter an integer; try again!")
        else:
            break
    data = dicts[index]
    corrected = {}
    for key, value in data.items():
        if key == 'personID':
            corrected[key] = value
        else:
            corrected[key] = input(
                    f"  {key} was <{data[key]}> change to: ")
            if not key == 'statusID':
                corrected[key] = f"'{corrected[key]}'"
    _ = quote_nonID_fields(data)
    print(f"original version: {repr(data)}")
    _ = input(f"corrected version: {repr(corrected)}")
    f_new = ', '.join([f"{key} = {value}" for
                key, value in corrected.items()])
    f_original = ' AND '.join([f"{key} = {value}" for
                key, value in data.items()])
    queries = []
    queries.append( f""" UPDATE Person_Status
            SET {f_new}
            WHERE {f_original}
            ; """)
    for query in queries:
        _ = input(query)



def new_status(report=None):
    """
    Make a single brand new entry in the Person_Status table.
    """
    prompt = "Running new_status()..."
    dicts = get_stati(prompt, report=report)
    if isinstance(dicts, int):
        report.append("No prior entries found.")
        print(report[-1])
        d = {'personID': dicts, }
    else:
        d = {'personID': dicts[1]['personID'], }
    for key in ('statusID', 'begin', 'end'):
        response = input(f"{key}: ")
        if not response: continue
        d[key] = response
        if key == 'statusID':
            d[key] = str(d[key])
        else:
            d[key] = f"'{d[key]}'"
    d["personID"] = str(d["personID"])
    field_names = [key for key in d.keys()]
    values = [value for value in d.values()]
    _ = input(f"{repr(d)}")
    query = f"""
            INSERT INTO Person_Status
            ({', '.join(field_names)})
            VALUES
            ({', '.join(values)})
            ;
            """
    _ = input(query)

def change_Person_Status_table(personID):
    """

    """
    menu_d = {
            "New status": new_status,
            "Update status": update_status,
            "Change status": change_status,
            }
    ret = ["Beginning status_change_cmd...", ]
    helpers.choose_and_run(menu_d, report=ret)
    return ret

def test4emptylisting():
    nonID = 655
    entries = status_entries4(nonID)
    if not entries:
        print(f"no status entries for personID {nonID}")
    else:
        print(f"got status entries for personID {nonID}")
    print(repr(entries))
    

def test_get_stati():
    while True:
        yn = input("\nProceed with test_get_stati? (y/n): ")
        if yn and yn[0] in "yY":
            res = get_stati("make a choice")
            if isinstance(res, dict):
                print("Got results as follows...")
                for k, v in res.items():
                    print(f"{k}: {v}")
            elif res == None:
                print("No personID found.")
            elif isinstance(res, int):
                print(f"'{res}' is an invalid personID")
            else:
                assert(False)
        else:
            break
def test_status_entries4():
    for d in status_entries4(97):
        for key, value in d.items():
            print(f"{key}: {value}; ", end='')
        print()

def test_update_status():
    update_status()

if __name__ == '__main__':
    test_update_status()
#   test_status_entries4()
#   test4emptylisting()
#   for s in status_choices():
#       print(s)
#   test_get_stati()
#   for line in status_change_cmd():
#       print(line)
#   status_change_cmd()
