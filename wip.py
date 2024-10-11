#!/usr/bin/env python3

# File: wip.py  (work in progress, for development)

"""
window types:
    collect a record/dict
        use code/textual/get_fields()
    choose from a listing of options/strings
                            functions
        use code/textual/menu()
Currently working on setting up the Dues table
for the upcoming year: delete non members and
add dues to all members.
NOTE: there's also a wip.py file in code directory.
"""

import csv
import PySimpleGUI as sg
from code import club
from code import helpers
from code import routines
from code import textual
from code import show
from code import data_entry

today = helpers.eightdigitdate
dues = club.yearly_dues

def update_dues_table(report=None):
    """
    Prepare Dues Table for upcoming Club year.

    """
    # create a set of memberIDs:
    query = routines.import_query("Sql/memIDs_f.sql")
    members = routines.fetch(query.format(today, today),
                            from_file=False)
    memberIDs = {entry[0] for entry in members}
#   print("memberIDs: " + repr(memberIDs))
    # set of inducties still owing:
    appIDs_owing = routines.fetch("Sql/appIDs_owing.sql")
    appIDs_owing = {item[0] for item in appIDs_owing}
#   print("appIDs_owing: " + repr(appIDs_owing))
    # now get a set of those who should be in the Dues table
    dues_paying = memberIDs | appIDs_owing
    #set of IDs currently in Dues table
    duesIDs = {entry[0] for entry in 
            routines.fetch(
            "SELECT personID, dues_owed FROM Dues;",
            from_file=False)}
    # delete non dues_paying peopleIDs from Dues Table:
    entries2delete = duesIDs - dues_paying
#   print("duesIDs: " + repr(duesIDs))
#   print("dues_paying: " + repr(dues_paying))
    n = 0
    for ID in entries2delete:
        query = f"DELETE FROM Dues WHERE personID = {ID};"
        yn = input(f"{query} OK?")
        if yn and yn[0] in "yY":
            routines.fetch(query,
                from_file=False, commit=True)
        n += 1
    # update set of IDs currently in Dues table
    old_duesIDs = duesIDs
    duesIDs = {entry[0] for entry in 
            routines.fetch(
            "SELECT personID, dues_owed FROM Dues;",
            from_file=False)}
    if not n: assert old_duesIDs == duesIDs
    for ID in dues_paying:
        # club.yearly_dues ==> Dues table
        if ID in duesIDs: # UPDATE Dues table
            query = f"""UPDATE Dues 
                    SET dues_owed = dues_owed + {dues}
                    WHERE personID = {ID};"""
#           print(query)
#           yn = input("Is the above query ok? (y/n) ")
            routines.fetch(query, from_file=False, commit=True)
        else: # New entry: INSERT INTO Dues table
            query = f"""INSERT INTO Dues
                    (personID, dues_owed)
                    VALUES ({ID}, {dues});"""
#           print(query)
#           yn = input("Is the above query ok? (y/n) ")
            routines.fetch(query, from_file=False, commit=True)

# The following are for the future: to prepare for the
# 2025 ==> 2026 billing cycle....
# As of 2024-04-06 amounts owed are already entered.

def update_kayak_slots_table(report=None):
    """
    <slot_cost> already filled out
    """
    pass

def update_dock_privileges_table(report=None):
    """
    <cost> already filled out
    """
    pass

def update_moorings_table(report=None):
    """
    <owing> already filled out
    """
    pass

def ck_members_f():
    query = "Sql/members_f.sql"  # personID is [0]
    print(query)
    query = routines.import_query(query)
    query = query.format(helpers.eightdigitdate,
                        helpers.eightdigitdate)
#   print(query)
    res = routines.fetch(query, from_file=False)
    print(f"Number of members: {len(res)}")
    s1 = {item[0] for item in res}

    query = "Sql/mem4join_ff.sql" # personID is [-1]
    print(query)
    query = routines.import_query(query)
    query = query.format(helpers.eightdigitdate,
                        helpers.eightdigitdate)
#   print(query)
    res = routines.fetch(query, from_file=False)
    s2 = {item[-1] for item in res}
    print(f"Number of members: {len(res)}")

    print(s2 - s1)


def for_Angie():
    """
    Creates a csv file of members exclusive
    of those who have announced retirement.
    """
    today = helpers.eightdigitdate
    big_list = routines.query2dict_listing(f"""
        SELECT P.personID, P.last, P.first, P.suffix
        FROM People as P
        JOIN Person_Status as PS
        WHERE P.personID = PS.personID
        AND ( 
            PS.statusID IN (11, 15)  -- New & Current Member
            AND ((PS.begin = '') OR (PS.begin <= {today}))
            AND((PS.end = '') OR (PS.end > {today}))
            )
        ORDER BY P.last, P.first""")
    little_list = routines.query2dict_listing(f"""
        SELECT P.personID, P.last, P.first, P.suffix
        FROM People as P
        JOIN Person_Status as PS
        WHERE P.personID = PS.personID
        AND ( 
            PS.statusID = 17  -- exclude retirees
            AND ((PS.begin = '') OR (PS.begin <= {today}))
            AND((PS.end = '') OR (PS.end > {today}))
            )
        ORDER BY P.last, P.first""")
    final_list = [item for item in big_list
                        if not item in little_list]
#   helpers.save_db(big_list, "4Angie.csv")
#   helpers.save_db(little_list, "4Angie.csv")
    helpers.save_db(final_list, "4Angie.csv")

def check_change_mapping():
    mapping = {"First": "Alex", "Last": "Kleider",
            "b_day": "",}
    mapping = textual.change_mapping(mapping)
    print("The following is being returned:")
    print(repr(mapping))
    pass

if __name__ == "__main__":
#   check_change_mapping()
    pass
    data_entry.change_status_cmd()
#   for_Angie()
#   table = "People"
#   fname = "members.csv"
#   routines.table2csv(table, fname)
#   ck_members_f()
#   report = []
#   update_dues_table(report)

