#!/usr/bin/env python3

# File: wip.py  (work in progress, for development)

"""
window types:
    collect a record/dict
        use code/textual/get_fields()
    choose from a listing of options/strings
                            functions
        use code/textual/menu()

# Code being developed here eventually to be
# moved into code/textual.py
"""

import PySimpleGUI as sg
from code import helpers
from code import routines
from code import textual

def params(one, two, kw1="kw1", kw2='kw2'):
    print(f"one: {one}")
    print(f"two: {two}")
    print(f"kw1: {kw1}")
    print(f"kw2: {kw2}")

def test_params():
    params(two=2, one=1, kw1="KW1", kw2="KW2")

# the following (app_keys, date_keys and app_query) are
# used by choose_applicant and some by get_key_val2change
app_keys = ("personID, last, first, suffix,"  # 4
      + " sponsor1ID, sponsor2ID,"      # +2 = 6 or -8
      + " app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,"
      + " approved, dues_paid, notified").split(", ")
date_keys = app_keys[6:]
app_query = """ -- current applicants
    SELECT P.personID, P.last, P.first, P.suffix,
        A.sponsor1ID, A.sponsor2ID, A.app_rcvd, A.fee_rcvd,
        A.meeting1, A.meeting2, A.meeting3, approved,
        dues_paid, notified
    FROM People as P JOIN Applicants as A
    WHERE A.personID = P.personID
    AND A.notified = "";"""


def choose_applicant(report=None):
    """
    Offers a menu/choice of all current applicants.
    Returns a dict representing chosen applicant
    OR None if no choice made (possibly no applicants.)
    """
    routines.add2report(report,
            "Entering 'choose_applicant' function...")
    # first query current applicants...
    res = routines.query2dict_listing(app_query,
        routines.keys_from_query(app_query), from_file=False)
    n_res = len(res)
    routines.add2report(report,
        f"...found {n_res} applicants from which to choose...")
    if n_res == 0: return  # return None if no applicants
    # set up mapping for the menu function
    mapping = {}
    for entry in res:
        if entry['suffix']: suffix = f' [{suffix.strip()}]'
        else: suffix = ''
        key = (f'{entry["personID"]:>4d} {entry["last"]}, '
            + f'{entry["first"]}' + suffix)
#       limited_entry = {}
#       for k in date_keys:
#           limited_entry[k] = entry[k]
#       mapping[key] = limited_entry
        mapping[key] = entry
    routines.add2report(report,
        "...returning from 'choose_applicant' function.")
    # use menu function to choose (and return) applicant
    return textual.menu(mapping, report=report,
            headers=["Current Applicants", "Pick an applicant"])

def get_key_val2change(mapping, report=None):
    """
    Presents a dialog box containing <mapping>'s key/value pairs.
    Returns a mapping of any key/value pairs that were changed...
    or None if nothing changed or user "CANCEL"s.
    """
    if not mapping: # { choose_applicant
        return        # { might return None
    routines.add2report(report,
        "Entering 'get_key_val2change' function...")
    ret = textual.change_or_add_values(mapping,
        report=report,
        headers=["Applicant Data", "Change or add an item..."])
    if not ret:
        routines.add2report(report,
            "...'get_key_val2change' returning None.")
        return
#   helpers.print_key_value_pairs(mapping)
#   helpers.print_key_value_pairs(ret)
    changes = {}
    for key in mapping.keys():
        if str(mapping[key]) != str(ret[key]):
#           print(f"{key}: '{mapping[key]}' != '{ret[key]}'")
            changes[key] = ret[key]
    if changes:
        routines.add2report(report,
            "...'get_key_val2change' returning changes.")
        return changes
    else:
        routines.add2report(report,
            "...'get_key_val2change' made no changes")


def query2update_applicant_table(personID, mapped_changes,
                            report=None):
    """
    Returns a query to update the Applicant table.
    """
    query = f"""UPDATE Applicants SET
            {{}}
            WHERE personID = {personID};"""
    entries = ', '.join([f"{key} = {value}" for key, value in
            mapped_changes.items()])
    return query.format(entries)


if __name__ == "__main__":
    report = []
    chosen_applicant = choose_applicant(report)
    personID = chosen_applicant["personID"]
    changes = get_key_val2change(chosen_applicant, report)
    if changes:
        print(
            query2update_applicant_table(personID,
                changes, report))
#       print("Changes to be made:")
#       for key, value in changes.items():
#           print(f"{key}: {value}")
    else:
        print('User "CANCEL"ed.')
    pass
    yn = input("Show report? y/n: ")
    if yn and yn[0] in "yY":
        for line in report:
            print(line)
#   test_params()
#   _ = input("W)ork i)n P)rogress...  Any key to continue")

