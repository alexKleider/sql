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
# used by choose_applicant and some by add_applicant_date
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
    # keys of the dict expected to be returned:
#   _ = input(f"keys: {repr(app_keys)}")
#   _ = input(f"date_keys: {repr(date_keys)}")
    # first query current applicants...
    routines.add2report(report,
            "Entering 'choose_applicant' function...")
    res = routines.query2dict_listing(app_query,
                            app_keys, from_file=False)
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

def add_applicant_date(applicant, report=None):
    if not applicant: # { choose_applicant
        return        # { might return None
    routines.add2report(report,
        "Entering 'add_applicant_date' function...")
    options = {key: value for (key, value) in }
    pass
    routines.add2report(report,
        "...returning from 'add_applicant_date' function.")

if __name__ == "__main__":
    report = []
    ret = choose_applicant(report)
    for key, value in ret.items():
        print(f"{key}: {value}")
    yn = input("Show report? y/n: ")
    if yn and yn[0] in "yY":
        for line in report:
            print(line)
#   test_params()
#   _ = input("W)ork i)n P)rogress...  Any key to continue")

