#!/usr/bin/env python3

# File: applicant_table.py

"""
Provides routines dealing with the applicant table.
Will also be writing ot other tables such as:
    Person_Status, Dues_Owed, ...
"""

import sys
from code import helpers
from code import routines

cur_applicants_query = """
    SELECT P.personID, P.first, P.last,
        A.sponsor1ID, S1.first, S1.last,
        A.sponsor2ID, S2.first, S2.last,
        A.app_rcvd, A.fee_rcvd,
        A.meeting1, A.meeting2, A.meeting3,
        A.approved, A.dues_paid, A.notified
    FROM people as P,
        Applicants as A,
        people as S1,
        people as S2
    WHERE P.personID = A.personID
    AND A.sponsor1ID = S1.personID
    AND A.sponsor2ID = S2.personID
    AND A.notified = ""
    ;
    """

def insert_new_applicant():
    pass

def current_applicants():
    """
    Returns a (possibly empty) listing tuples:
    one for each applicant.
    """
    return routines.fetch(cur_applicants_query, from_file=False)

def cur_app_dicts():
    """
    Returns a (possibly empty) listing of dicts:
    one for each applicant.
    """
    gen = routines.dicts_from_query(cur_applicants_query,
                                    keys=None,
                                    replace_periods=True)
    return [dict(d) for d in gen]


def matchID2applicant(appID, applicants):
    """
    Returns <applicant> with ID <appID>
    or None if no applicants or no match
    <applicants> is a list of dicts or iterables.
    """
    if not applicants:
        print("No applicants provided to match!")
        return
    try:
        if iter(applicants[0]):  # iterables
            for applicant in applicants:
                if applicant[0] == appID:
                    return applicant
    except TypeError:  # it's a list of dicts, not tuples!
        for applicant in applicants:
            if applicant["P_personID"] == appID:
                return applicant
    _ = input("matchID2applicant(): No match found!")
    return  # ?no match found #


def rtn_applicantID(current_applicants):
    """
    Returns an applicant ID or
    none if none selected/available.
    """
    if not current_applicants:
        _ = input("No applicants! (Rtn to continue) ")
        return
    appIDs = {app[0] for app in current_applicants}
    while True:
        header = "Choose an applicantID from one of the following:"
        print("=" * len(header)); print(header); print("=" * len(header));
        for entry in current_applicants:
            print(f"  {entry}")
        appID = input("Choose applicant ID: (0 to quit) ")
        try:
            appID = int(appID)
        except ValueError:
            print("!! Must be an integer !!")
            continue
        if appID == 0:
            _ = input("select_applicantID aborted!")
            return
        if appID in appIDs:
            return appID
        else:
            print(f"{appID=}  {appIDs}")

def rtn_applicant(applicants):
    """
    <applicants> can be a list of dicts or tuples.
    Returns the chosen  dict or tuple, or
    None if no choice made.
    """
    if not applicants:
        print("No applicants provided to match!")
        return
    while True:
        print("++++++++++++++++++++")
        print("Choose a personID (0 to quit):  ")
        IDs = set()
        d = {}
        index = 0
        if isinstance(applicants[0], dict):
            for applicant in applicants:
                print("Dict values...")
                print([ value for value in applicant.values()])
                IDs.add(applicant["P_personID"])
                d[applicant["P_personID"]] = applicant
                index += 1
        else:
            for applicant in applicants:
                print(applicant)
                IDs.add(applicant[0])
                d[applicant[0]] = applicant
                index += 1
        id_chosen = int(input("Enter ID of choice... "))
        if id_chosen == 0:
            return
        if id_chosen in IDs:
            return d[id_chosen]


def update_applicant():
    applicants = current_applicants()
    apID = rtn_applicantID(applicants)
    for applicant in applicants:
        if apID == applicant[0]:
            return applicant

if __name__ == "__main__":
#   print(update_applicant())
#   print(rtn_applicantID(current_applicants()))
#   print(update_applicant())
#   print(routines.keys_from_query(cur_applicants_query,
#                                  replace_periods=True))
    print("applicant for applicant in current_applicants()")
    for applicant in current_applicants():
        print(applicant)
    print()
    print("applicant dicts...")
    cur_apps = cur_app_dicts()
#   print(cur_apps)
    for d in cur_apps:
        print(d)
    print("#######################################")
    print("Running with tuples...")
    applicants = current_applicants()
    print(rtn_applicant(applicants))
    print("#######################################")
    print("Running with dicts...")
    applicants = cur_app_dicts()
    print(rtn_applicant(applicants))





