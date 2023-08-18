#!/usr/bin/env python3

# File: update.py

"""
Prototyping a status_change_cmd
    update_status  {  the two choices
    add_status     {  under development
Notes:
    application comes in
        +/- application fee
    1st meeting
    2nd meeting
    3rd meeting
    approval 
    dues
    am => m (one year later)
"""

from code import helpers
from code import routines

status_keys = routines.get_keys_from_schema("Stati")
ps_keys = routines.get_keys_from_schema("Person_Status")

def status_choices():
    """
    Returns a list of strings:
    a listing of header and all available stati with their
    statusID, code and text (to serve as a reference.)
    """
    res = routines.fetch("SELECT * FROM Stati;",
            from_file=False)
    ret = ["Stati from which to choose:",
           "===========================",
           ]
    for entry in res:
        ret.append(entry)
    return ret

def entries_for_ID(personID):
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


def set_up(prompt, report=None):
    """
    Prompts for and collects a personID.
    Returns A: a dict: a dict of dicts- to serve as a 'menu':
        1 based integer keys, dict for each value.
    OR B: an integer: personID (if no previous entries found.)
    """
    if isinstance(report, list):
        report.append("Entering update.setup(prompt)")
    print(prompt)
    rec = routines.pick_People_record()
    if not rec:
        _ = input("record not found")
        return
    else:
        personID = rec['personID']
        print("Stati from which to choose:")
        for line in status_choices():
            print(f"  {line}")
        entries = entries_for_ID(rec["personID"])
        dicts = dict(zip(range(1, len(entries)+1), entries))
        if not dicts:  # no previous entries
            return personID
        return dicts

def update_status(report=None):
    """
    Update an existing entry.
    """
    prompt = "Running update_status()..."
    dicts = set_up(prompt, report=report)
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
    query = f""" UPDATE Person_Status
            SET {f_new}
            WHERE {f_original}
            ; """
    _ = input(query)


def enter_status(report=None):
    """
    Make a brand new entry.
    """
    prompt = "Running enter_status()..."
    dicts = set_up(prompt, report=report)
    if isinstance(dicts, int):
        report.append("No prior enties found.")
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

def status_change_cmd():
    ret = ["Beginning status_change_cmd...", ]
    menu_d = {
            "Update": update_status,
            "New entry": enter_status,
            }
    helpers.choose_and_run(menu_d, report=ret)
    return ret

def test4emptylisting():
    entries = entries_for_ID(300)
    dicts = dict(zip(range(1, len(entries)+1), entries))
    if not dicts:
        print("dicts is empty")
    print(repr(dicts))
    


if __name__ == '__main__':
#   test4emptylisting()

    for line in status_change_cmd():
        print(line)
