#!/usr/bin/env python3

# File: update.py

"""
Prototyping a status_change_cmd
"""

from code import helpers
from code import routines

status_keys = routines.get_keys_from_schema("Stati")
ps_keys = routines.get_keys_from_schema("Person_Status")

def status_choices():
    """
    Returns a list of strings.
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
    query = f"""
        SELECT * from Person_Status WHERE personID = {personID};
        """
    res = routines.fetch(query, from_file=False)
#   print("entries_for_ID returns:")
#   _ = input(res)
   
    ret = []
    for entry in res:
        ret.append(dict(zip(ps_keys, entry)))
    return ret

def set_up(prompt, report=None):
    """
    Returns a "menu": a dict of dicts-
    1 based integer keys, dict for each value.
    If no previous entry found, then an integer is returned:
    the personID chosen.
    """
    if report:
        report.append(prompt)
#   print(report[-1])
    rec = routines.pick_People_record()
    if not rec:
        _ = input("record not found")
        return
    else:
        personID = rec['personID']
        print("Stati from which to choose:")
        for line in status_choices():
            print(f"  {line}")
#       print("Entries already there:")
#       ret = []
        entries = entries_for_ID(rec["personID"])
#       _ = input(f"{repr(entries)}")
        dicts = dict(zip(range(1, len(entries)+1), entries))
#       _ = input(f"{repr(dicts)}")
#       for key, value in dicts.items():
#           print(f"{key:>3}: {repr(value)}")
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
    index = int(input("Which entry needs changed? "))
    data = dicts[index]
    corrected = {}
    for key, value in data.items():
        if key == 'personID':
            corrected[key] = value
        else:
            corrected[key] = input(f"  {key} was <{data[key]}> change to: ")
            if not key == 'statusID':
                corrected[key] = f"'{corrected[key]}'"
    print(f"corrected version: {repr(corrected)}")

def enter_status(report=None):
    """
    Make a brand new entry.
    """
    prompt = "Running enter_status()..."
    dicts = set_up(prompt, report=report)
    if isinstance(dicts, int):
        print("No prior enties founc")
        d = {'personID': dicts, }
    else:
        d = {'personID': dicts[1]['personID'], }
    for key in ('statusID', 'begin', 'end'):
        response = input(f"{key}: ")
        if not response: continue
        d[key] = response
        if not key == 'statusID':
            d[key] = f"'{d[key]}'"
    field_names = [key for key in d.keys()][1:]  # { no need for
    values = [value for value in d.values()][1:] # {  personID
#   _ = input(f"{repr(d)}")
    query = f"""
            INSERT INTO Table
            ({', '.join(field_names)})
            VALUES
            ({', '.join(values)})
            WHERE personID = {d['personID']};
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

if __name__ == '__main__':
    for line in status_change_cmd():
        pass
#       print(line)
