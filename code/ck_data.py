#!/usr/bin/env python3

# File: ck_data.py

"""
Provides ck_data.consistency_report (for menu.py.)
Module for routines that check for data consistency, specifically:
    google data "labels"/contacts match sql Person_Status table
        applicant == statiID 1..10
        DockUsers
        GaveUpMembership
        inactive
        Kayak
        LIST == members (stati 11 & 15)
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

holder = club.Holder()

# The following queries are for comparison with Google
# contacts 'Labels' i.e. those without email are excluded.
queries = dict(
    # We've no intention of accepting applicants without email!
    applicant="""SELECT P.first, P.last, P.suffix
        FROM people as P
        JOIN Applicants as A
        WHERE A.personID = P.personID
            AND A.notified = ''
            -- excludes those that are no longer applicants
        ;""",
    GaveUpMembership="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 27, 28)
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
                AND PS.statusID in (11, 15)
                AND NOT P.email = ''
                AND (PS.end = '' OR PS.end > {})
                AND (PS.begin = '' OR PS.begin < {})
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
    expired="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 26
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

dock_query = """SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Dock_Privileges as DP
            WHERE P.personID = DP.personID
            ;"""
mooring_query = """SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Moorings as M
            WHERE P.personID = M.personID
                AND NOT P.email = ''
            ;"""



def get_gmail_record(g_rec):
    """
    Returns a "g_dict" (only the info we need.)
    Client is yield_contacts.
    <g_rec> is a record from the gmail contacts file.
    NB: google calls them 'Labels', referred to here as 'groups'.
    "g_" prefix refers to google contact data.
    """
    g_email = g_rec["E-mail 1 - Value"]
    group_membership = (
        g_rec["Group Membership"].split(" ::: "))
    if (group_membership and
            group_membership[-1] == '* myContacts'):
        group_membership = group_membership[:-1]
    return dict(
        first = g_rec["Given Name"],
        last = g_rec["Family Name"],
        suffix = g_rec["Name Suffix"],
        g_email=g_email,
        groups=set(group_membership),
        )

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
            yield get_gmail_record(g_rec)

def members_and_applicants_filter(g_dict):
        if ({"LIST", "applicant", "inactive"} &
                g_dict['groups']):
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
    Possible groups/labels: applicant, Committee, DockUsers,
    everyone, expired, GaveUpMembership, inactive, Kayak, LIST,
    Moorings, Officers, Outer Basin Moorers, secretary, 
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
applicants_and_members = (3,4,5,6,7,8,9,10,11,14,15,16,17)

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
    keys = "first, last, suffix".split(', ')
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
    if not g_data['name_w_gmail'] == m_data['name_w_email']:
        report.extend(['',
            "Gmail and People table emails don't match!..."])
        only_gmail = sorted(g_data['name_w_gmail'] -
                m_data['name_w_email'])
        if only_gmail:
            report.append("Entries in Gmail not in sql db:")
            for item in only_gmail:
                report.append(f'\t{item}')
        only_sql = sorted(m_data['name_w_email'] -
                    g_data['name_w_gmail'])
        if only_sql:
            report.append("Entries in sql db not in Gmail:")
            for item in only_sql:
                report.append(f'\t{item}')
    else:
        report.append("...OK")
    return report

def consistency_report(report=None):
    """
    Called by menu.py under Reports/check_data_consistency
    """
    if not report:
        report = []
    report.extend(ck_m_vs_g_data())
    report.extend(mooring_dock())
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


if __name__ == '__main__':
    for line in consistency_report([]): 
        print(line)
#   for line in ck_m_vs_g_data():
#       print(line)
#   ck_gather_contacts_data()
#   res = gather_member_data()
    

