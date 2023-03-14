#!/usr/bin/env python3

# File: utils.py

"""
Plan is to eventually merge this code into code/commands.py
and delete this file once that's done.
To do that, need to replace APP_KEY_VALUES with equivalent
data gleaned from a query of the Stati table!
See Notes/infrastructure.txt

General:
    initDB, closeDB, fetch_query
Applicant related:
    getApplicants, appl_dicts, appl_status
    appsByStatus, 
"""

import sqlite3

club_db = "/home/alex/Git/Sql/Secret/club.db"


def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("clubcursor")
    """
    try:
        db = sqlite3.connect(path)
        clubcursor = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:", path)
        db, clubcursor = None, None
        raise
    return db, clubcursor


def closeDB(database, cursor):
    try:
       cursor.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise
 

def fetch_query(cursor, query, message=None):
    """Returns fetchall() after running the query"""
    try:
        cursor.execute(query)
        ret = cursor.fetchall()
    except sqlite3.OperationalError:
        if message:
            print(message)
        else:
            print(
              f"The following query failed:\n{query}\n======")
        return None
        raise
#   print(f"fetch_query returning\n{ret}")
    return ret


def getAppStatiDict():
    """
    creates a dict to take the place of APP_KEY_VALUES 
    """
    with open('Sql/get_app_stati.sql', 'r') as infile:
        query = infile.read()
    db, cursor = initDB(club_db)
    res = fetch_query(cursor, query)
    ret = {}
    for line in res:
        ret[line[1]] = line[2]
    return ret

stati_key_values = getAppStatiDict()
'''
APP_KEY_VALUES = {  # Souldn't be any need for this: 
    # the SPoT should be the Stati table!
    "a-": "Application received without fee", #0
    "a" : "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ad": "Inducted & notified, membership pending payment of dues",
    "m": "New Member",  # temporary until congratulatory letter.
    }

The following returned Mar 11, '23
         Key   Value
         ===   =====
           a:  Application complete but not yet acknowledged
          a-:  Application received without fee
          a0:  Applicant (no meetings yet)
          a1:  Attended one meeting
          a2:  Attended two meetings
          a3:  Attended three (or more) meetings
          ad:  Inducted & notified, membership pending payment of dues
          ai:  Inducted, needs to be notified
          am:  New Member
          av:  Vacancy ready to be filled pending payment of dues
          aw:  Inducted & notified, awaiting vacancy
          ba:  Postal address => mail returned
          be:  Email on record being rejected
           h:  Honorary Member
           i:  Inactive (continuing to receive minutes)
           m:  Member in good standing
           r:  Retiring/Giving up Club Membership
           t:  Membership terminated (probably non payment of fees)
           w:  Fees being waived
     z1_pres:  President
       z2_vp:  VicePresident
      z3_sec:  Secretary of the Club
z4_treasurer:  Treasurer
    z5_d_odd:  Director- term ends Feb next odd year
   z6_d_even:  Director- term ends Feb next even year
         zae:  Application expired or withdrawn
         zzz:  No longer a member
'''


def getApplicants(cursor):
    """
    Retrieves _all_ applicant data (incl. demographics)
    except those who have become members
    or have dropped out ('zae').
    """
    with open("Sql/getApplicants.sql", 'r') as infile:
        query = infile.read()
#   print("Executing following query...")
#   print(query)
#   _ = input()
    return fetch_query(cursor, query,
            message="Sorry getApplicants.sql failed")


def appl_dicts(cursor):
    """
    returns a dict of dicts, one for each applicant
    (that has not yet become a member or dropped out)
    (keyed by applicant's personID)
    """
    res = getApplicants(cursor)
    appl_keys = (
        "personID", "first", "last", "suffix", 'phone',
        'address', 'town', 'state', 'postal_code', 'email',
        "sponsor1", "sponsor2",
        "app_rcvd", "fee_rcvd",
        "meeting1", "meeting2", "meeting3",
        "approved", "inducted", "dues_paid"
        )
    ret = dict()
    for line in res:
        z = zip(appl_keys, line)
        ret[line[0]] = {key: value for key, value in z}
    return ret

def appl_status(appl_dict):
    """
    Taking data (appl_dict) derived from the Applicants table
    (which contains sponsors & dates) returns the relavant
    Stati table key.
    <appl_dict> must have at a minimum the following keys:
    app_rcvd, fee_rcvd, meeting1..3, approved & dues_paid
    returning:
    'a-', 'a', 'a1', 'a2', 'a3', 'ad', 'm' or None
    A return of None suggests something is wrong!!!
    What if applicant drops out?
    Data could be inconsistent!!
    Must insure consistency between Applicants and
    Person_Status tables!!!!
    """
    if (appl_dict['app_rcvd']
    and not appl_dict['fee_rcvd']):
        return 'a-'
    elif (appl_dict['fee_rcvd']
    and not appl_dict['meeting1']):
        return 'a' 
    elif (appl_dict['meeting1']
    and not appl_dict['meeting2']):
        return 'a1' 
    elif (appl_dict['meeting2']
    and not appl_dict['meeting3']):
        return 'a2' 
    elif (appl_dict['meeting3']
    and not appl_dict['approved']):
        return 'a3' 
    elif (appl_dict['approved']
    and not appl_dict['dues_paid']):
        return 'ad' 
    elif appl_dict['dues_paid']:
        return 'm'
    else:
        return None


def prSortedAppDict():
    db, cur = initDB(club_db)
    ap_ds = appl_dicts(cur)
    for key in sorted([key for key in ap_ds.keys()]):
        values = [value for value in ap_ds[key].values()]
        print(f"{key:>3}: {values}\n")
    closeDB(db, cur)


def appsByStatus(appdict):
    """
    Parameter is what's returned by appl_dicts(cursor)
    Returns a dict keyed (and sorted) by status key.
    Each value is a dict of values pertaining to an applicant.
    """
    ret = {}
    for personID in sorted([key for key in appdict]):
        d = appdict[personID]
        s= appl_status(d)
        _ = ret.setdefault(s, [])
        ret[s].append(d)
    return ret


web_formatter = (
    "{address}, {town}, {state} {postal_code} [{email}]")

report_formatter = ("{first} {last}" + '\n' +
        '    ' + "Sponsors: {sponsor1}, {sponsor2}" + '\n    '
        + "Meetings: {meeting1} {meeting2} {meeting3}" )


applicant_formatter = (web_formatter + '\n' +
        '    ' + "Sponsors: {sponsor1}, {sponsor2}" + '\n    '
        + "Meetings: {meeting1} {meeting2} {meeting3}" )


def display_apsByStatus(apsbystatus, formatter=None):
    """
    This code should be modified to use a query rather
    than rely on APP_KEY_VALUES.
    """
    ret = []
    for status in [key for key in apsbystatus.keys()]:
        text = stati_key_values[status]
        header = ['\n'+text, '-'*len(text)]
        ret.extend(header)
        for entry in apsbystatus[status]:
            if not formatter:
                ret.append(', '.join([str(value) for value in
                    entry.values()]))
            else:
                ret.append(formatter.format(**entry))
    return ret


def applicantReport():
    db, cur = initDB(club_db)
    ap_ds = appl_dicts(cur)
    closeDB(db, cur)
    n_applicants = len(ap_ds)
    header = f'Applicants ({n_applicants} in number)'
    report = [header, '='*len(header)]
    ap_by_status = appsByStatus(ap_ds)
    report.extend(display_apsByStatus(ap_by_status,
        formatter=report_formatter))
    return '\n'.join(report)


def main():
    print(applicantReport())


def main():
    d = getAppStatiDict()
    ret = ['         Key   Value',
           '         ===   =====',
           ]
    for key, value in [(key, value) for (key, value) in d.items()]:
        ret.append(f'{key:>12}:  {value}')
    print('\n'.join(ret))


if __name__ == '__main__':
    main()

