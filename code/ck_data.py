#!/usr/bin/env python3

# File: ck_data.py

"""

Module for routines that check for data consistency, specifically:
    google data "labels" match sql Person_Status table
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
    everyone with an email is in the google data base
Began with already existing code in $CLUBU/data.py
"""

import os
import sys
import csv
import json

import club
import helpers
import routines


DEBUGGING_FILE = 'debug.txt'

# The following queries are for comparison with Google
# contacts 'Labels' i.e. those without email are excluded.
queries = dict(
    # We've no intention of accepting applicants without email!
    applicant="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Applicants as A
            WHERE A.personID = P.personID
                AND A.notified = ''
            ;""",
    GaveUpMembership="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 27)
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
            ;""".format(helpers.eightdigitdate),
    Officers="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
              AND PS.statusID IN (20, 21, 22, 23, 24, 25, 28)
              AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    secretary="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 22
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
    # used by gather_contacts_data #
    <g_rec> is a record from the gmail contacts file.
    Returns a dict with only the info we need.
    """
    g_email = g_rec["E-mail 1 - Value"]
    group_membership = (
        g_rec["Group Membership"].split(" ::: "))
    if (group_membership and
            group_membership[-1] == '* myContacts'):
        group_membership = group_membership[:-1]
    group_membership = set(group_membership)
    first_name = " ".join((
        g_rec["Given Name"],
        g_rec["Additional Name"],
        )).strip()
    last_name = " ".join((
        g_rec["Family Name"],
        g_rec["Name Suffix"],
        )).strip()
#   gname = "{}, {}".format(last_name, first_name)
    gname = "{},{}".format(last_name, first_name)
    alias = "{}{}".format(first_name, last_name)
    muttname = '{} {}'.format(first_name, last_name)
    return dict(
        gname=gname,
        alias=alias,
        muttname=muttname,
        g_email=g_email,
        groups=group_membership,
        )


def gather_contacts_data(club):    # used by ck_data #
    """
    The club attributes populated:
        gmail_by_name,
        groups_by_name,
        g_by_group.
    All values are sets.
    Names are all 'last,first_suffix'
    """
    club.gmail_by_name = dict()  # => string
    club.groups_by_name = dict()  # => set

    club.g_by_group = dict()  # >set of names

    # Traverse contacts.csv => g_by_name
    with open(club.contacts_spot, 'r',
        encoding='utf-8', newline='') as file_obj:
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}"...'
            .format(file_obj.name))
        for g_rec in google_reader:
            g_dict = get_gmail_record(g_rec)

            club.gmail_by_name[g_dict['gname']] = g_dict['g_email']
            club.groups_by_name[g_dict['gname']] = g_dict['groups']

            for key in g_dict["groups"]:
                _ = club.g_by_group.setdefault(key, set())
                club.g_by_group[key].add(g_dict["gname"])



def get_dict(source_file, sep=":", maxsplit=1):
    """
    # used by gather_extra_fees_data #
    A generic function to parse files.
    Blank lines or comments ('#') are ignored.
    All other lines must contains a 'first last' name followed by
    a separator (<sep> defaults to ':') and then anything else.
    Returned is a dict keyed by 'last,first' name and value: the
    string to right of <sep> (stripped of leading &/or trailing
    spaces. (It could be an empty string!)
    # Applicant data is populated one line at a time so this
    # function is not useful there
    """
    ret = {}
    with open(source_file, 'r') as stream:
        for line in stream:
            line = line.strip()
            if not line or line[0] == '#': continue
            parts = line.split(sep=sep, maxsplit=maxsplit)
            if len(parts) != 2:
                assert False, "Error in code/ck_data."
            names = parts[0].split()
            try:
                name_key = '{},{}'.format(names[1], names[0])
            except IndexError:
                _ = input("IndexError re line: '{}'"
                        .format(line))
            ret[name_key] = parts[1].strip()
    return ret


def ck_data(club):
    """
    Check integrity/consistency of of the Club's data bases:
    1.  MEMBERSHIP_SPoT  # the main club data base
    2.  CONTACTS_SPoT    # csv downloaded from gmail
    3.  APPLICANT_SPoT   #
    4.  SPONSORS_SPoT    #
    5.  EXTRA_FEES_SPoTs #
        ...
    The first 4 of the above all contain applicant data
    and must be checked for consistency.  Data in the 2nd
    and 5th must be consistent with that in the 1st.
    
    Returns a report (an array of lines) which (if <fee_details>
    is set to True) can be extended to include any discrepencies
    between what's billed each year vs what is still owed:
    useful after payments begin to come in.

    Consistency checks required:
    -memlist-    names emails stati&fees  which_fee&amt
    -contacts-   names emails  labels
    -sponsors-   names (all sponsors are members?) 
    -applicants- names        stati
    -extra_fees- names                    which_fee&amt
    [1] in future may keep records of non (no longer) members (and
    expired applicants.)
    """
#   print("Entering data.ck_data")
    club.ret = []
    club.ok = []
    club.varying_amounts = []
    club.not_matching_notice = ''
    helpers.add_header2list("Report Regarding Data Integrity",
                club.ret, underline_char='#', extra_line=True)
    gather_membership_data(club)  # from main data base
    gather_contacts_data(club)  # club gmail account contacts
    gather_extra_fees_data(club)  # data comes from SPoTs
    populate_sponsor_data(club)
    populate_applicant_data(club)
    club.applicants_by_status = get_applicants_by_status(club)


    ## First check that google groups match club data:
    # Deal with extra fees...
    ck_malformed(club)
    ck_fee_paying_labels(club)  # google groups vs club data
    ck_fees_spots(club)  # mem list vs extra fees SPoT
    # Keep in mind that after payment amounts won't match
    # Can use '-d' options for details.

    ck_gmail(club)


    ## do we compare gmail vs memlist emails anywhere????
    ## None of the following are populated!!!
    email_problems = []
    missing_emails = []
    non_member_contacts = []

    redact4now = '''
    if non_member_contacts:
        helpers.add_sub_list(
            "Contacts without a corresponding Member email",
            non_member_contacts, club.ret)
    else:
        club.ok.append('No contacts that are not members.')
    pass
    emails_missing_from_contacts = []
    common_emails = []

    if emails_missing_from_contacts:
        helpers.add_sub_list("Emails Missing from Google Contacts",
                         emails_missing_from_contacts, club.ret)
    else:
        club.ok.append("No emails missing from gmail contacts.")
'''

    ck_applicants(club)

    if club.ok:
        helpers.add_sub_list(
            "No Problems with the Following", club.ok, club.ret)
    ai_notice = "Acceptable Inconsistency"
    if club.not_matching_notice:
        helpers.add_header2list(ai_notice,
                                club.ret, underline_char='=')
        club.ret.append(club.not_matching_notice)
    if club.varying_amounts:
        helpers.add_header2list(
            "Fee Disparities: probably some have paid",
            club.ret, underline_char='-', extra_line=True)
        club.ret.extend(club.varying_amounts)
    return club.ret




def data_listed(data, underline_char='=', inline=False):
    """
    Assumes 'data' is a dict with list values.
    Returns a list of lines: each key as a header +/- underlining
    followed by its values one per line, or (if 'inline'=True) on
    the same line separated by commas after a colon.
    """
    ret = []
    keys = sorted(data.keys())
    for key in keys:
        values = sorted(data[key])
        if inline:
            ret.append(key + " :" + ", ".join(values))
        else:
            ret.append("\n" + key)
            ret.append(underline_char * len(key))
            ret.extend(values)
    return ret


def applicant_set():
    """
    Returns set of lsst/first names of current applicants.
    """
    query = """SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Applicants as A
            WHERE A.personID = P.personID
                AND A.notified = '';
    """
    applicants = []
    keys = "first, last, suffix".split(', ')
    res = routines.fetch(query, from_file=False)
    for item in res:
        d = helpers.make_dict(keys, item)
        if d['suffix']:
            d['last'] = d['last'] + '_' + d['suffix'].strip()
        applicants.append(f"{d['last']},{d['first']}")
    app_set = set(applicants)
    assert(len(app_set) == len(applicants)), 'Error in ck_data.applicant_set'
    return app_set
    for entry in applicants:
        print(entry)
    pass
    

def display_google_contact_data():
    print("data.py compiles without errors.")
    holder = club.Holder()
    gather_contacts_data(holder)
    print("\n== gmail_by_name ==")
    for key, value in holder.gmail_by_name.items(): 
        print(f"{key}: {value}")
    _ = input()
    print("\n== groups_by_name ==")
    for key, value in holder.groups_by_name.items():
        print(f"{key}: {value}")
    _ = input()
    print("\n== g_by_group ==")
    for key, value in holder.g_by_group.items():
        print(f"{key}: {value}")

def ck_labels():
    """
    """
    report = []
    keys = "first, last, suffix".split(', ')
    report = []
    holder = club.Holder()
    gather_contacts_data(holder)
    labels = [key for key in queries.keys()]
#   print(f"labels: {labels}")
#   print(holder.g_by_group['applicant'])
#   print(holder.g_by_group['inactive'])
    for label in labels:
#       print(f"Dealing with: {label}")
        category_lst = []
        res = routines.fetch(queries[label],from_file=False)
        for item in res:
            d = helpers.make_dict(keys, item)
            if d['suffix']:
                d['last'] = (d['last'] + '_' +
                        d['suffix'].strip())
            category_lst.append(f"{d['last']},{d['first']}")
        category_set = set(category_lst)
        if len(category_set) != len(category_lst):
            report.append(f"""
Error condition regarding {label}:
    set:  {category_set}
    should be the same length as
    list: {category_lst}
                """)
        if category_set != holder.g_by_group[label]:
            _ = input(f"""The following do _not_ match:
                db {label}: {sorted(category_set)}
            and
            google {label}: {sorted(holder.g_by_group[label])}
            """)
            dif = (category_set -
                    holder.g_by_group[label])
            _ = input(f"{dif}")
            dif = (holder.g_by_group[label] -
                    category_set)
            _ = input(f"{dif}")
        else:
            report.append(f"Labels match stati for {label}")
    return report

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

def consistency_report():
    report = []
    report.extend(ck_labels())
    report.extend(mooring_dock())
    return report


if __name__ == '__main__':
#   display_google_contact_data()
    for line in consistency_report(): 
        print(line)
    pass





