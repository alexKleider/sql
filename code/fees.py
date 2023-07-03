#!/usr/bin/env python3

# File: code/fees.py

"""
Provides data from Dues,
            Dock_Privileges,
            Kayak_Slots and
            Moorings tables.
"""

import csv
import sqlite3
try: from code import routines
except ImportError: import routines
try: from code import helpers
except ImportError: import helpers

tables = ('Dues', 'Dock_Privileges', 'Kayak_Slots', 'Moorings')
dues_file_name = 'dues.csv'
dock_file_name = 'dock_use_fees.csv'
kayak_file_name = 'kayak_storage_fees.csv'
mooring_file_name = 'mooring_fees.csv'

def get_dues(owing_only=True, report=None):
    selection = "personID, first, last, dues_owed"
    query = """
        SELECT P.personID, P.first, P.last, D.dues_owed
        FROM People as P
        JOIN Dues as D
        ON P.personID = D.PersonID
        JOIN Person_Status AS PS
        ON P.personID = PS.personID
        JOIN Stati as St
        ON St.statusID = PS.statusID
        WHERE St.statusID in (11, 15)
        AND PS.end < {}
        -- must format: use code.helpers.sixdigitdate
        ORDER BY P.last, P.first, P.suffix ; """
    query = query.format(helpers.sixdigitdate)
    if not report==None:
        if owing_only:
            report.append("getting dues still owing")
        else:
            report.append(
                    "getting dues (including zero balances)")
    res = routines.fetch(query, from_file=False)
    dict_listing = []
    for item in res: 
        record = routines.make_dict(
                selection.split(', '), item)
        if not owing_only or record["dues_owed"] != 0:
            dict_listing.append(record)
    return dict_listing

def get_dock(owing_only=True, report=None):
    selection = "personID, first, last, cost"
    query = """SELECT P.personID, P.first, P.last, D.cost
            FROM People as P
            JOIN Dock_Privileges AS D
            ON P.personID = D.personID
            ORDER BY P.last, P.first
            """
    if not report==None:
        if owing_only:
            report.append("getting docking fees still owing")
        else:
            report.append(
                "getting docking fees (including zero balances)")
    res = routines.fetch(query, from_file=False)
    dict_listing = []
    for item in res:
        record = routines.make_dict(
                selection.split(', '), item)
        if not owing_only or record["cost"] != 0:
            dict_listing.append(record)
    return dict_listing


def get_kayak(owing_only=True, report=None):
    selection = "personID, first, last, slot_cost"
    query = """SELECT P.personID, P.first, P.last, K.slot_cost
            FROM People as P
            JOIN Kayak_Slots as K
            ON P.personID = K.personID
            ORDER BY P.last, P.first
            """
    if not report==None:
        if owing_only:
            report.append("getting kayak storage fees still owing")
        else:
            report.append(
        "getting kayak storage fees (including zero balances)")
    res = routines.fetch(query, from_file=False)
    dict_listing = []
    for item in res:
        record = routines.make_dict(
                selection.split(', '), item)
        if not owing_only or record['slot_cost'] != 0:
            dict_listing.append(record)
    return dict_listing


def get_mooring(owing_only=True, report=None):
    selection = ("personID, first, last, "
                + "mooring_code, mooring_cost, owing")
    if report!=None:
        if owing_only:
            report.append("getting mooring fees still owing")
        else:
            report.append(
                "getting mooring fees (including zero balances)")
    res = routines.fetch("Sql/mooring2.sql")
    dict_listing = []
    for item in res: 
        record = routines.make_dict(
                selection.split(', '), item)
        if not owing_only or record["owing"] != 0:
            dict_listing.append(record)
    return dict_listing


def check_balances(progress_listing):
    while True:
        print("=====================")
        yn = input("Owing only? (y/n) ")
        if yn and yn[0] in 'yY': owing_only = True
        else: owing_only = False
        choice = routines.get_menu_response(tables,
                header="Choose one of the following",
                incl0Q=True)
        if choice == 0: break
        elif choice == 1:
            helpers.dump2csv_file(get_dues(owing_only),
                    dues_file_name)
            print(f"File '{dues_file_name}' created.")
        elif choice == 2:
            helpers.dump2csv_file(get_dock(owing_only),
                    dock_file_name)
            print(f"File '{dock_file_name}' created.")
        elif choice == 3:
            helpers.dump2csv_file(get_kayak(owing_only),
                    kayak_file_name)
            print(f"File '{kayak_file_name}' created.")
        elif choice == 4: 
            helpers.dump2csv_file(get_mooring(owing_only),
                    mooring_file_name)
            print(f"File '{mooring_file_name}' created.")
        else:  # routines.get_menu_response won't allow this
            print("invalid choice; '0' to quit")
    


if __name__ == '__main__':
    ret = []
    check_balances(ret)
