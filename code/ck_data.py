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
    Client is gather_contacts_data.
    <g_rec> is a record from the gmail contacts file.
    Returns a "g_dict" (only the info we need.)
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


def gather_contacts_data():    # used by ck_data #
    """
    Gets data from gmail contacts and returns 
    three dicts:  see first 4 lines of code
    """
    ret = {}
    ret['gmail_by_name'] = dict()  # => string (email)
    ret['groups_by_name'] = dict()  # => set of groups
    ret['g_by_group'] = dict()  # >set of names

    # Traverse contacts.csv => g_by_name
    with open(holder.contacts_spot, 'r',
        encoding='utf-8', newline='') as file_obj:
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}"...'
            .format(file_obj.name))
        for g_rec in google_reader:
            g_dict = get_gmail_record(g_rec)
            name_key = "{last}, {first}".format(**g_dict)
            if g_dict['suffix']:
                name_key = name_key + ' ' + g_dict['suffix']
            ret['gmail_by_name'][name_key] = g_dict['g_email']
            ret['groups_by_name'][name_key] = g_dict['groups']
            for key in g_dict["groups"]:
                _ = ret['g_by_group'].setdefault(key, set())
                ret['g_by_group'][key].add(name_key)
    return ret


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


def ck_data(holder):
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
    holder.ret = []
    holder.ok = []
    holder.varying_amounts = []
    holder.not_matching_notice = ''
    helpers.add_header2list("Report Regarding Data Integrity",
                holder.ret, underline_char='#', extra_line=True)
#   gather_membership_data(holder)  # from main data base
    gather_contacts_data(holder)  # club gmail account contacts
#   gather_extra_fees_data(holder)  # data comes from SPoTs
#   populate_sponsor_data(holder)
#   populate_applicant_data(holder)
#   holder.applicants_by_status = get_applicants_by_status(holder)


    ## First check that google groups match club data:
    # Deal with extra fees...
#   ck_malformed(holder)
#   ck_fee_paying_labels(holder)  # google groups vs club data
#   ck_fees_spots(holder)  # mem list vs extra fees SPoT
    # Keep in mind that after payment amounts won't match
    # Can use '-d' options for details.

#   ck_gmail(holder)


    ## do we compare gmail vs memlist emails anywhere????
    ## None of the following are populated!!!
    email_problems = []
    missing_emails = []
    non_member_contacts = []

    redact4now = '''
    if non_member_contacts:
        helpers.add_sub_list(
            "Contacts without a corresponding Member email",
            non_member_contacts, holder.ret)
    else:
        holder.ok.append('No contacts that are not members.')
    pass
    emails_missing_from_contacts = []
    common_emails = []

    if emails_missing_from_contacts:
        helpers.add_sub_list("Emails Missing from Google Contacts",
                         emails_missing_from_contacts, holder.ret)
    else:
        holder.ok.append("No emails missing from gmail contacts.")
'''

#   ck_applicants(holder)

    if holder.ok:
        helpers.add_sub_list(
            "No Problems with the Following", holder.ok, holder.ret)
    ai_notice = "Acceptable Inconsistency"
    if holder.not_matching_notice:
        helpers.add_header2list(ai_notice,
                                holder.ret, underline_char='=')
        holder.ret.append(holder.not_matching_notice)
    if holder.varying_amounts:
        helpers.add_header2list(
            "Fee Disparities: probably some have paid",
            holder.ret, underline_char='-', extra_line=True)
        holder.ret.extend(holder.varying_amounts)
    return holder.ret




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
    

def google_contacts_report(holder=holder):
    """
    All google data in a human readable form.
    """
    report = []
    gather_contacts_data(holder)
    report.append("== gmail_by_name ==")
    sub_report = []
    for key, value in holder.gmail_by_name.items(): 
        sub_report.append(f"{key}: {value}")
    report.extend(sorted(sub_report))
    report.append("\n== groups_by_name ==")
    sub_report = []
    for key, value in holder.groups_by_name.items():
        sub_report.append(f"{key}: {value}")
    report.extend(sorted(sub_report))
    report.append("\n== g_by_group ==")
    sub_report = []
    for key, value in holder.g_by_group.items():
        sub_report.append(f"\n{key}: {sorted(value)}")
    report.extend(sorted(sub_report))
    fname = input("Enter file name or '' if to std out: ")
    if fname:
        with open(fname, 'w') as outf:
            for line in report:
                outf.write(line+'\n')
    else:
        for line in report:
            print(line)
    return report


def ck_labels(holder=holder):
    """
    """
    report = []
    keys = "first, last, suffix".split(', ')
    gather_contacts_data(holder)
    labels = [key for key in queries.keys()]
#   print(f"labels: {labels}")
#   print(holder.g_by_group['applicant'])
#   print(holder.g_by_group['inactive'])
    for label in labels:
        report.append(f"Dealing with: {label}")
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
            category_lst.sort()
            duplicates = []
            for i in range(1, len(category_lst)):
                if category_lst[i] == category_lst[i-1]:
                    duplicates.append(category_lst[i])
            if duplicates:
                report.append(f"Duplicates in {label}: {duplicates}")
            redact = '''
            report.append(f"""
Error condition regarding {label}:
    set:  {sorted(category_set)}
    should be the same length as
    list: {sorted(category_lst)}
                """)
            '''
            report.append(f"len(category_set): {len(category_set)}")
            report.append(f"len(category_lst): {len(category_lst)}")




        try:
            g_by_group = holder.g_by_group[label]
        except IndexError:
            report.extend([
                f"There are no google label '{label}' entries",
                f"to compare to {repr(category_set)}.",
                ])
        else:
            if category_set != g_by_group:
                _ = input(f"""The following do _not_ match:
                    db {label}: {sorted(category_set)}
                and
                google {label}: {sorted(holder.g_by_group[label])}
                """)
                dif = (category_set -
                        holder.g_by_group[label])
                _ = input(f"{sorted(dif)}")
                dif = (holder.g_by_group[label] -
                        category_set)
                _ = input(f"{sorted(dif)}")
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

def consistency_report(report, holder=holder):
    """
    """
    report.extend(ck_data(holder))
    report.extend(ck_labels())
    report.extend(mooring_dock())
    return report


if __name__ == '__main__':
#   google_contacts_report()
#   for line in consistency_report([]): 
#       print(line)

    data = gather_contacts_data()
    for key in data.keys():
        _ = input(key)
        for k, v in data[key].items():
            print(f'{k}: {v}')
        _ = input("^^^^^" + key)
    

