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

query1 = """ -- current applicants
        SELECT P.personID, P.last, P.first, 
                A.meeting1, A.meeting2, A.meeting3
        FROM People as P
        JOIN Applicants as A
        WHERE A.personID = P.personID
        AND A.notified = ""
    ;"""

def current(report):
    routines.add2report(report,
            "Working on 'current' function...")
    res = routines.fetch(query1, from_file=False)
    n_res = len(res)
    routines.add2report(report,
            f"...presenting {n_res} options...")
    mapping = {}
    for line in res:
#       key = f"{res[0]:4d>} {res[1]:}, {res[2]:}"
        key = f"{line[0]:>4d} {line[1]}, {line[2]}"
#       value = line[0]
#       mapping[key] = value
        mapping[key] = key
    routines.add2report(report,
            "...finished working on 'current' function.")
    return textual.menu(mapping, report=report,
            headers=["Member Listing", "Pick a member"])

if __name__ == "__main__":
    report = []
    ret = current(report)
    yn = input(f"Returned '{ret}'; show report? y/n: ")
    if yn and yn[0] in "yY":
        for line in report:
            print(line)
#   test_params()
#   _ = input("W)ork i)n P)rogress...  Any key to continue")

