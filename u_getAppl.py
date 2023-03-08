#!/usr/bin/env python3

# File: u_getAppl.py

import sqlite3

"""
appl_status()
STATI_REGISTERED_IN_Stati_TABLE
query2find_applicants 
result_of_query2find_applicants 
stati_in_use 
APPLICANT_STATI = {  # only those to be used in current system
NON_APPLICANT_STATI = {
appl_keys = (
initDB()
try_query(cursor, query):


"""

dbpath = "/home/alex/Git/Sql/Secret/"
club_db = "club.db"

def appl_status(appl_dict):
    """
    <appl_dict>: a dict with the following keys:
    app_rcvd, fee_rcvd, meeting1..3, approved & dues_paid
    returning:
    'a-', 'a', 'a1', 'a2', 'a3', 'ad', 'm' or None
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


## the following is a product of
#  query:  SELECT * FROM Stati; 
STATI_REGISTERED_IN_Stati_TABLE = """
1|a-|Application received without fee
2|a|Application complete but not yet acknowledged
3|a0|Applicant (no meetings yet)
4|a1|Attended one meeting
5|a2|Attended two meetings
6|a3|Attended three (or more) meetings
7|ai|Inducted, needs to be notified
8|ad|Inducted & notified, membership pending payment of dues
9|av|Vacancy ready to be filled pending payment of dues
10|aw|Inducted & notified, awaiting vacancy
11|am|New Member
12|be|Email on record being rejected
13|ba|Postal address => mail returned
14|h|Honorary Member
16|i|Inactive (continuing to receive minutes)
17|r|Retiring/Giving up Club Membership
18|t|Membership terminated (probably non payment of fees)
19|w|Fees being waived
20|z1_pres|President
21|z2_vp|VicePresident
22|z3_sec|Secretary of the Club
23|z4_treasurer|Treasurer
24|z5_d_odd|Director- term ends Feb next odd year
25|z6_d_even|Director- term ends Feb next even year
26|zae|Application expired or withdrawn
27|zzz|No longer a member
"""

result_of_query2find_applicants = """
119|John|Maalis||Albert Foreman|George Krakauer|220315|220315|220506|220701|221007|||
151|Caleb|Norton||Ed Mann|John Norton|220805|220902|220902|221007|230203|||
58|Kingston|Dixon||Bob MacDonald|Rupert Dixon|220805|220902|220902|221007|230203|||
143|Lorelei|Morris||Ralph Camiccia|Terry Camiccia|220915|220915|221202|230106|230303|||
171|Lorin|Rich||Ed Mann|Ralph Camiccia|221007|221007|221104|230106|230203|||
46|Jake|Cortez||William Norton|Daniel Speirn|230203|221007|230203|||||
91|Eric|Joost||Billy Cummings|Sandy Monteko-Sherman|221221|221221||||||
29|Sandra|Buckley||Billy Cummings|Sandy Monteko-Sherman|221221|221221|||230303|||
"""

stati_in_use = """
29|Sandra|Buckley|a1
34|Angie|Calpestri|z4_treasurer
35|Ralph|Camiccia|z5_d_odd
46|Jake|Cortez|a1
58|Kingston|Dixon|a3
64|Jay|Eickenhorst|i
70|Rudi|Ferris|z5_d_odd
91|Eric|Joost|a0
119|John|Maalis|a3
120|Bob|MacDonald|z6_d_even
124|Ed|Mann|z3_sec
135|Jeff|McPhail|z5_d_odd
143|Lorelei|Morris|a3
144|Don|Murch|z5_d_odd
151|Caleb|Norton|a3
159|Kenny|Paasch|ba
171|Lorin|Rich|a3
179|Peter|Sandmann|i
205|Kirsten|Walker|z6_d_even
62|Mark|Dolen|z1_pres
135|Jeff|McPhail|z2_vp
109|Paul|Krohn|zzz
"""

APPLICANT_STATI = {  # only those to be used in current system
    "a-": "Application received without fee", #0
    "a0": "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ad": "Inducted & notified, membership pending payment of dues",
    }

NON_APPLICANT_STATI = {
    "be": "Email on record being rejected",   # => special notice
    "ba": "Postal address => mail returned",  # => special notice
    "h" : "Honorary Member",                             #10 > #12
    'm' : "Member in good standing",
    'i' : "Inactive (continuing to receive minutes)",
    'r' : "Retiring/Giving up Club Membership",
    "w" : "Fees being waived",  # a rarely applied special status
    'z1_pres': "President",
    'z2_vp': "VicePresident",
    'z3_sec': "Secretary of the Club",
    'z4_treasurer': "Treasurer",
    'z5_d_odd': "Director- term ends Feb next odd year",
    'z6_d_even': "Director- term ends Feb next even year",
    'zae': "Application expired or withdrawn",
    'zzz': "No longer a member"
    }


def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("theClub")
    """
    try:
        db = sqlite3.connect(path)
        theClub = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:",
                path)
        db, theClub = None, None
        raise
    return db, theClub

def try_query(cursor, query):
    try:
        cursor.execute(query)
        ret = cursor.fetchall()
    except sqlite3.OperationalError:
        print(f"The following query failed:\n{query}\n======")
        return None
        raise
    return ret

def closeDB(database, theClub):
    try:
       theClub.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise
       

def get_appl(cursor):
    """
    Returns result of query2find_applicants
    """
    query2find_applicants = """ SELECT
            P.personID, P.first, P.last, P.suffix,
            A.sponsor1, A.sponsor2,
            app_rcvd, fee_rcvd,
            A.meeting1, A.meeting2, A.meeting3,
            A.approved, A.inducted, A.dues_paid
        FROM Applicants as A
        JOIN People as P
        WHERE A.personID = P.personID
        ;"""
    try:
        cursor.execute(query2find_applicants)
    except sqlite3.OperationalError:
        print("'query2find_applicants' failed")
        raise
    res = cursor.fetchall()
    return res

def applicant_dict_by_id():
    """
    Returns a dict version of what's returned by
    query2find_applicants
    """
    appl_keys = (
        "personID", "first", "last", "suffix", 
        "sponsor1", "sponsor2",
        "app_rcvd", "fee_rcvd",
        "meeting1", "meeting2", "meeting3",
        "approved", "inducted", "dues_paid"
        )
    db, cursor = initDB(dbpath+club_db)
    res = get_appl(cursor)
    ret = dict()
    for line in res:
        z = zip(appl_keys, line)
        ret[line[0]] = {key: value for key, value in z}
    return ret

def show_appl_dict_by_id(applicant_dict_by_id):
    for key in applicant_dict_by_id.keys():
        value = [value for value in applicant_dict_by_id[key].values()]
        print(f"{key:>3}: {value}")

def get_nonmember_stati_in_use():
    query2get_nonmember_stati_in_use = """
    SELECT P.personID, P.first, P.last, P.suffix, S.key
    FROM People AS P
    JOIN Person_Status as PS
    JOIN Stati AS S 
    WHERE P.personID = PS.personID
    AND PS.statusID = S.statusID
    AND NOT S.key = 'm';  -- exclusive of members
        -- otherwise result is too long!
        -- NOTE: includes members with stati other than 'm'.
    """
    res = """
(29, 'Sandra', 'Buckley', '', 'a1')
(34, 'Angie', 'Calpestri', '', 'z4_treasurer')
(35, 'Ralph', 'Camiccia', '', 'z5_d_odd')
(46, 'Jake', 'Cortez', '', 'a1')
(58, 'Kingston', 'Dixon', '', 'a3')
(64, 'Jay', 'Eickenhorst', '', 'i')
(70, 'Rudi', 'Ferris', '', 'z5_d_odd')
(91, 'Eric', 'Joost', '', 'a0')
(119, 'John', 'Maalis', '', 'a3')
(120, 'Bob', 'MacDonald', '', 'z6_d_even')
(124, 'Ed', 'Mann', '', 'z3_sec')
(135, 'Jeff', 'McPhail', '', 'z5_d_odd')
(143, 'Lorelei', 'Morris', '', 'a3')
(144, 'Don', 'Murch', '', 'z5_d_odd')
(151, 'Caleb', 'Norton', '', 'a3')
(159, 'Kenny', 'Paasch', '', 'ba')
(171, 'Lorin', 'Rich', '', 'a3')
(179, 'Peter', 'Sandmann', '', 'i')
(205, 'Kirsten', 'Walker', '', 'z6_d_even')
(62, 'Mark', 'Dolen', '', 'z1_pres')
(135, 'Jeff', 'McPhail', '', 'z2_vp')
(109, 'Paul', 'Krohn', '', 'zzz')
"""
    ### Note: 'm' for member, not included! ###
    db, cursor = initDB(dbpath+club_db)
    try:
        cursor.execute(query2get_nonmember_stati_in_use )
    except sqlite3.OperationalError:
        print("'query2get_nonmember_stati_in_use' failed")
        raise
    res = cursor.fetchall()
    ret = {}
    keys = (  # not used
        'personID', 'first', 'last', 'suffix', 'status_key',)
    for line in res:
        key = line[-1]
        _ = ret.setdefault(key,[])
        ret[key].append(line[:-1])
    return ret


def get_appl_stati_from_Stati():
    pass



if __name__ == '__main__':
#   print(
#   "Running 'show_appl_dict_by_id(applicant_dict_by_id())':")
#   show_appl_dict_by_id(applicant_dict_by_id())
    print("\nRunning 'get_nonmember_stati_in_use()'")
    ret = get_nonmember_stati_in_use()
#   _ = input(ret)
    print("and printing key: value for")
    print("each item of the returned dict:")
    keys = sorted(ret.keys())
    for key in keys:
        print(f"\n{key:>12}:")
        for item in ret[key]:
            print(item)
#   db, cursor = initDB(dbpath+club_db)
#   app_by_id = applicant_dict_by_id()
#   appl_stati(app_by_id )
#   for applicant in app_by_id:
#       pass

#   keys = sorted(ret.keys())
#   for key in keys:
#       print(f"{key:>12}: {ret[key]} ({len(ret[key])})")
#   closeDB(db, cursor)
