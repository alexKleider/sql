#!/usr/bin/env python3

# File: ck_data.py

"""
Provides ck_data.consistency_report (for menu.py.)
Module to check for data consistency, specifically:
    google data "labels"/contacts match sql Person_Status table
        applicant == statiID 1..10
        dropped
        DockUsers
        GaveUpMembership
        inactive
        Kayak
        LIST == members (stati 11, 15 & 17)
        Moorings
        Officers == statiID 20..25:  z[123456]* 
        Outer Basin Moorers
        secretary
        Committee
    everyone with an email is in the google data base

Began with already existing code in $CLUBU/data.py
"""

import os
import sys
import csv
import json

try: from code import club
except ImportError: import club
try: from code import helpers
except ImportError: import helpers
try: from code import routines
except ImportError: import routines

# LABELS will have to be updated whenever
# there's a change made to gmail contacts...
LABELS = set("""applicant dropped Committee DockUsers everyone
 GaveUpMembership inactive Kayak LIST Moorings Officers
 Outer_Basin_Moorers_2023 secretary""".split())

holder = club.Holder()

# The following queries are for comparison with Google
# contacts 'Labels' i.e. those without email are excluded
# since they wouldn't be amongst google contacts.
queries = dict( # indexed by google contacts LABELs.
    # We've no intention of accepting applicants without email!
    applicant="""SELECT P.first, P.last, P.suffix
        FROM people as P
        JOIN Applicants as A
        WHERE A.personID = P.personID
            AND A.notified = ''
            AND NOT P.email = ''
            -- excludes those that are no longer applicants
        ;""",
    GaveUpMembership="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (27, 28)
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            -- Terminated, No longer a member
            ; """.format(helpers.eightdigitdate),
    # Unlikely we'll accept inactive status
    # for someone without email...
    inactive="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 16
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            ;""".format(helpers.eightdigitdate),
    LIST="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (11, 15, 17)
                AND NOT P.email = ''
                AND (PS.end = '' OR PS.end > {})
                AND (PS.begin = '' OR PS.begin <= {})
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate),
    Officers="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
              AND PS.statusID IN (20, 21, 22, 23, 24, 25, 29)
              AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    secretary="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 22
                AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    Committee="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 30
                AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    dropped="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 26)
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            ;""".format(helpers.eightdigitdate),
    DockUsers="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Dock_Privileges as DP
            WHERE P.personID = DP.personID
                AND NOT P.email = ''
            ;""",
    Kayak="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Kayak_Slots as KS
            WHERE P.personID = KS.personID
                AND NOT P.email = ''
            ;""",
    Moorings="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Moorings as M
            WHERE P.personID = M.personID
                AND NOT P.email = ''
            ;""",
    )

for_later = '''
queries['Outer Basin_Moorers -2023'] = """
            SELECT P.first, P.last, P.suffix
            FROM people as P
            """
'''

dock_query = """SELECT P.personID, P.first, P.last, P.suffix
            FROM people as P
            JOIN Dock_Privileges as DP
            WHERE P.personID = DP.personID ;"""
kayak_query = """SELECT K.slot_code, K.slot_cost, P.personID,
                        P.first, P.last, P.suffix
            FROM people as P
            JOIN Kayak_Slots as K
            WHERE P.personID = K.personID
            ORDER by P.last, P.first;"""
mooring_query = """SELECT P.personID, P.first, P.last, P.suffix
            FROM people as P
            JOIN Moorings as M
            WHERE P.personID = M.personID ;"""
members4dues = """SELECT P.personID  -- must get rid
            FROM people as P         -- of retirees!
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND (PS.statusID in (11, 15)
                    AND (PS.end = '' OR PS.end > {})
                    AND (PS.begin = '' OR PS.begin <= {}))
            ORDER BY P.personID
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate) 
retirees =  """SELECT P.personID
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND (PS.statusID = 17   -- retiring
                    AND (PS.end = '' OR PS.end > {})
                    AND (PS.begin = '' OR PS.begin <= {}))
            ORDER BY P.personID
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate) 
dues_listing = """SELECT personID from Dues
            ORDER by personID;"""

def get_gmail_record(g_rec):
    """
    Returns a "g_dict" (only the info we need.)
    Client is yield_contacts.
    <g_rec> is a record from the gmail contacts file.
    NB: google calls them 'Labels'.
    "g_" prefix refers to google contact data.
    Returns None if g_rec is without Lables
    ### NOTE: Google changed keys in contacts ~2024/07 !!!!
    ### Resulted in key_error !!!!
    """
    g_email = g_rec["E-mail 1 - Value"]
#   _ = input(f"{repr(g_rec.keys())}")
#   if not "Group Membership" in g_rec.keys():
    if not "Labels" in g_rec.keys():
        return  # ignore gmail contacts that have no 'Label'
    labels = (  # a list
#       g_rec["Group Membership"].split(" ::: "))
        g_rec["Labels"].split(" ::: "))
    if (labels and
            labels[-1] == '* myContacts'):
        labels = labels[:-1]
        labels = set(labels)
#       print(f"In get_gmail_record, labels: {labels}")
        if "Retired" in labels:
            labels = (labels - {"Retired"}) | {"LIST"}
            print(f"{g_email}, {groups}")
        ret = dict(
            first = g_rec["First Name"],
            last = g_rec["Last Name"],
            suffix = g_rec["Name Suffix"],
            g_email=g_email,
            groups=labels,
            )
        return ret

def yield_contacts():
    """
    "yields" a dict (as defined by get_gmail_record)
    for each google contact.
    """
    with open(club.Holder.contacts_spot, 'r',
        encoding='utf-8', newline='') as file_obj:
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}"...'
            .format(file_obj.name))
        for g_rec in google_reader:
            ret = get_gmail_record(g_rec)
#           _ = input("{last}, {first}: {groups}"
#                               .format(**ret))
            if ret: yield ret

def members_and_applicants_filter(g_dict):
    set2include = {"LIST", "applicant", "inactive"}
#   if g_dict["email"] == "kmdibblee@gmail.com":
#   print(f"{g_dict['groups']}")  # ({'Kayak', 'LIST'},)
#   print(f"{set2include}")
    if set2include & g_dict['groups']:
        return True


def gather_contacts_data(filter_func=None):
    """
    Returns gmail contacts data (limited by <filter_func>
    if provided.)
    Returns a dict with 3 keys: 
        values: one is a set of strings (names and emails)
            other two are dicts
    ... see first 4 lines of code
    to compare sql data and google contacts data
    Possible groups/labels defined by LABELS (see above.)
    """
    ret = {}
    ret['name_w_gmail'] = set()  # => strings (names and email)
    ret['groups_by_name'] = dict()  # => set of groups
    ret['names_by_group'] = dict()  # >set of names
    # Traverse contacts.csv => g_by_name
    for g_dict in yield_contacts():
        name_key = "{last}, {first}".format(**g_dict)
        if g_dict['suffix']:
            name_key = name_key + ' ' + g_dict['suffix']
            # suffixes have ' ' prepended in the sql db
        if not filter_func or filter_func(g_dict):
            ret['name_w_gmail'].add(
                    name_key + ": " + g_dict['g_email'])
            ret['groups_by_name'][name_key] = g_dict['groups']
            for key in g_dict["groups"]:
                _ = ret['names_by_group'].setdefault(key, set())
                ret['names_by_group'][key].add(name_key)
    return ret

# stati2include possibilities:
applicants_and_members = (3,4,5,6,7,8,9,10,11,14,15,16)

# restriction possibilities:
not_email_restriction = " AND NOT email = '' "

def gather_member_data(stati2include=None,
                        restriction=False):
    """
    Collects data from the sql data base returning
    three dicts (similar to <gather_contacts_data()>)
    <stati2include> (an iterable of integers/statusIDs) if
    provided can limit what's returned.
    <restrictions> can be an optional clause to restrict
    what's returned by the query. 
    """
    query_on_line = ''
    if stati2include:
        listing = ','.join([repr(s) for s in stati2include])
        query_on_line = f"""PS.statusID in ({listing}) 
                AND
                """
    if not restriction:
        restriction = ""
    ret = {}  # member data
    ret['name_w_email'] = set()  # => strings (names and email)
    ret['stati_by_name'] = dict()  # => set of stati
    ret['names_by_status'] = dict()  # >set of names

    keys = "ID, last, first, suffix, email, status, end".split(', ')
    query = f"""
    SELECT P.personID, P.last, P.first, P.suffix, P.email,
        PS.statusID, PS.end
    FROM People as P
    JOIN Person_Status as PS 
    ON  (
        {query_on_line}
        PS.personID = P.personID)
    WHERE PS.end > {helpers.eightdigitdate} or PS.end = ''
        {restriction}   ;
    """
    res = routines.query2dict_listing(query,
                            keys, from_file=False)
    for d in res:
        name_key = "{last}, {first}".format(**d)
        if d['suffix']:
            name_key = name_key + d['suffix']
        ret['name_w_email'].add(
                name_key + ": " + d['email'])
        pass
    return ret


def mooring_dock():
    """
    Ensure that no one is charged for both mooring & dock usage.
    """
    report = []
    keys = "personID, first, last, suffix".split(', ')
    mooring = routines.fetch(mooring_query,from_file=False)
    dock = routines.fetch(dock_query,from_file=False)
    for res in [mooring, dock]:
        listing = []
        for item in res:
            d = helpers.make_dict(keys, item)
            if d['suffix']:
                d['last'] = (d['last'] + '_' +
                        d['suffix'].strip())
            listing.append(f"{d['last']},{d['first']}")
#       res = set(listing)
#   print(f"{mooring}")
#   print(f"{dock}")
    empty = set(mooring) & set(dock)
    if empty:
        report.append(
          "The following are common to both mooring and dock:")
        report.append(empty)
    else:
        report.append("No mooring & dock overlap.")
    return report


def compare(g_data, label, which_stati, report):
    # First check that all 'labels' exist...
    label_names = set(g_data['names_by_group'].keys())
    if not label in label_names:
        report.append(
            f"!!'{label}' not in {repr(label_names)}!!")
        return
    if label == "Outer_Basin_Moorers_2023":
        report.append(
            f"!!not dealing with '{label}'!!")
        return
    # ... passed the check
    res = routines.fetch(queries[label],
                        from_file=False)
    set_members = set([f"{a[1]}, {a[0]}{a[2]}" for
                    a in res])
    if not (set_members ==
            g_data['names_by_group'][label]):
        report.append(
            f"...{label} group doesn't match {which_stati}")
        report.extend(helpers.check_sets(set_members, 
                            g_data['names_by_group'][label]))
    else:
        report.append(
            f"...{label} group matches {which_stati}")


def ck_m_vs_g_data():
    """
    Compares member and applicant data for consistency between
    sql db and gmail contacts (including stati/labels as
    appropriate.) (Excludes those without emails since such
    members don't appear in the gmail data.)
    """
    report = []
    report.append(
        "Checking for gmail and sql db consistency...")
    g_data = gather_contacts_data(members_and_applicants_filter)
    m_data = gather_member_data(
                stati2include=applicants_and_members,
                restriction = not_email_restriction)
    # check that names and emails match:
    if g_data['name_w_gmail'] != m_data['name_w_email']:
        print(report[-1])
        report.extend(['',
            "Gmail and People table emails don't match!..."])
        report.extend(helpers.check_sets(
            g_data['name_w_gmail'], m_data['name_w_email'],
            header_in1st_not2nd=
                "Entries in Gmail not in sql db:",
            header_in2nd_not1st=
                "Entries in sql db not in Gmail:"))
    else:
        report.append("...emails consistent")
    # check that Labels/groups match stati..
    # need to lift restrictions to include all
    # (not just members and applicants!)
    g_data = gather_contacts_data()
    m_data = gather_member_data(
                restriction = not_email_restriction)
    # Applicants/applicant:
    compare(g_data, 'applicant', 'applicant_stati', report)
    # Members/LIST:
    compare(g_data, 'LIST', 'member_stati', report)
#   # Members/Retired:
#   compare(g_data, 'Retired', 'retired_stati', report)
    # Committee
    compare(g_data, 'Committee', 'comittee_stati', report)
    # DockUsers
    compare(g_data, 'DockUsers', 'dock_user_stati', report)
    # dropped
    compare(g_data, 'dropped', 'dropped_stati', report)
    # GaveUpMembership
    compare(g_data, 'GaveUpMembership', 'quit_stati', report)
    # inactive
    compare(g_data, 'inactive', 'inactive_stati', report)
    # Kayak
    compare(g_data, 'Kayak', 'kayak_stati', report)
    # Moorings
    compare(g_data, 'Moorings', 'moorings_stati', report)
    # Officers
    compare(g_data, 'Officers', 'officers_stati', report)
    # Outer_Basin_Moorers_2023
    compare(g_data, 'Outer_Basin_Moorers_2023',
                            'outer_moorings_stati', report)
    # secretary
    compare(g_data, 'secretary', 'secretary_stati', report)
    report.append("...end of gmail vs SQL consistency check")
    return report


def ck_appl_vs_status_tables():
    """
    Compares Applicants and Stati tables for consistency.
    Sql/aS.sql queries get info from Applicant table
    Sql/sS.sql queries get info from Status table
    "S" can be one of the following: 0, 1, 2, 3, d
    """
    fs = "{:0} {:1}, {:2}{:3}"
    report = []
    report.append(
        "Checking Applicant and Stati table consistency...")
    res_app_table = routines.fetch(
            "Sql/still_applicants.sql")
    res_app = [fs.format(*entry) for entry in res_app_table]
    res_status_table = routines.fetch(
            "Sql/applicants_from_stati.sql")
    res_status =  [fs.format(*entry) for entry in
                                        res_status_table]
    if res_app != res_status:
        report.extend(helpers.check_sets(
                set(res_app), set(res_status)))
    query_pairs = (
                ('Sql/a0-.sql', 'Sql/s0-.sql', ),
                ('Sql/a0.sql', 'Sql/s0.sql', ),
                ('Sql/a1.sql', 'Sql/s1.sql', ),
                ('Sql/a2.sql', 'Sql/s2.sql', ),
                ('Sql/a3.sql', 'Sql/s3.sql', ),
                ('Sql/ad.sql', 'Sql/sd.sql', ),
            )
    ok = True
    for a_query, s_query in query_pairs:
#   for n in range(len(queries)):
        res_a = routines.fetch(a_query)
        res_s = routines.fetch(s_query)
        if res_a != res_s:
            ok = False
            report.append(
                "Applicant and Person_Status table missmatch!")
            print(f"res_a: {res_a}")
            res_a = [' '.join(str(item)) for item in res_a]
            print(f"res_s: {res_s}")
            res_s = [' '.join(str(item)) for item in res_s]
            report.extend(helpers.check_sets(
                set(res_a), set(res_s),
                header_in1st_not2nd=
                f"in {a_query}, not {s_query}"))
#   if not ok:
#       report.append("Problems")
    report.append("... App/Stati consistency check done.")
    return report

def ck_members_vs_dues(report=None):
    if not report: report = []
    resa = routines.fetch(members4dues, from_file=False)
    resb = routines.fetch(retirees, from_file=False)
    sa = set([item[0] for item in resa])
    sb = set([item[0] for item in resb])
    s1 = sa - sb
    res2 = routines.fetch(dues_listing, from_file=False)
    s2 = set([item[0] for item in res2])
    if s1 != s2:
        report.append(
            "Member listing and Dues table missmatch:")
        report.append(
            f"In members not dues: {repr(sorted(s1-s2))}")
        for pID in s1 - s2:
            report.append(
                f"{routines.get_rec_by_ID(pID).values()}")
        report.append(
            f"In dues not members: {repr(sorted(s2-s1))}")
        for pID in s2 - s1:
            report.append(
                f"{routines.get_rec_by_ID(pID).values()}")
    else:
        report.append(
            "Member listing and Dues table correspond.")
    return report


def consistency_report(report=None):
    """
    Called by menu.py under Reports/check_data_consistency
    """
    if not report:
        report = []
    report.extend(ck_m_vs_g_data())
    report.extend(ck_appl_vs_status_tables())
    report.extend(mooring_dock())
    report.extend(ck_members_vs_dues())
    return report


def ck_gather_contacts_data(members_and_applicants_filter):
    data = gather_contacts_data()
    for key in data.keys():
        _ = input(f"{key} vvvvv")
        if isinstance(data[key], dict):
            for k, v in data[key].items():
                print(f'{k}: {v}')
            _ = input("^^^^^" + key)
        else:
            for item in sorted(data[key]):
                print(item)
            print("^^^^^^^")


def ck_stati_vs_labels():
    """
    Still a work in progress
    """
    contact_data = gather_contacts_data()
    groups_by_name = contact_data['groups_by_name']
    sql_data = gather_member_data()
    stati_by_name = sql_data['stati_by_name']

def get_kayak_listing():
    ret = routines.fetch(kayak_query, from_file=False)
    ret = sorted(ret)
    for entry in ret:
        print(f"    {entry[4]}, {entry[3]}")


if __name__ == '__main__':
    pass
#   get_kayak_listing()

#   for line in consistency_report([
#       "Consistency Report",
#       "=================="]): 
#       print(line)

#   for line in ck_appl_vs_status_tables():
#       print(line)

#   for line in ck_m_vs_g_data():
#       print(line)
#   ck_gather_contacts_data()
#   res = gather_member_data()
