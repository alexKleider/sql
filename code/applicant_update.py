#!/usr/bin/env python3

# File: applicant_update.py

"""
Provides routines dealing with the applicant table.
Will also be writing to other tables such as:
    Person_Status,  # implemented
    Dues_Owed,
    Receipts, 
    ...
"""

try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

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

def cur_app_dicts():
    """
    Returns a (possibly empty) listing of dicts:
    one for each applicant.
    """
    gen = routines.dicts_from_query(cur_applicants_query,
                                    keys=None,
                                    replace_periods=True)
    return [dict(d) for d in gen]

def insert_new_applicant():
    """ NOT USED yet """
    pass

def current_applicants():
    """
    NOT USED
    Returns a (possibly empty) listing tuples:
    one for each applicant.
    """
    return routines.fetch(cur_applicants_query, from_file=False)


def matchID2applicant(appID, applicants):
    """   NOT USED!!
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
    appIDs = {app["P_personID"] for app in current_applicants}
    while True:
        header = "Choose an applicantID from one of the following:"
        helpers.print_header(header, bracket=True)
        for entry in current_applicants:
            values = [value for value in entry.values()]
            print(f"  {[value for value in values]}")
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
        try:
            id_chosen = int(input("Enter ID of choice... "))
        except ValueError:
            print("Must enter an integer!!")
            continue
        if id_chosen == 0:
            return
        if id_chosen in IDs:
            return d[id_chosen]


def applicant2update(app_dicts):
    """
    Returns a dict selected from <ap_dicts>:
    user's choice of which applicant to update.)
    """
    apID = rtn_applicantID(app_dicts)
    for applicant in app_dicts:
        if apID == applicant["P_personID"]:
            return applicant


def first_empty_key(applicant):
    for key, val in applicant.items():
        if not applicant[key]:
            print(f"first_empty_key returning {key}")
            return key
def last_full_key(applicant):
    for key, val in applicant.items():
        if val: last_key = key
        if not applicant[key]:
            print(f"last_full_key returning {key}: {val}")
            return last_key

key2status = {
    # Date to add:  |     Status to update:
        "A_app_rcvd": 1,  #1|a-|Application received without fee
#                 2|a|Application complete but not yet acknowledged
        "A_fee_rcvd": 3,  #3|a0|No meetings yet
        "A_meeting1": 4,  #4|a1|Attended one meeting
        "A_meeting2": 5,  #5|a2|Attended two meetings
        "A_meeting3": 6,  #6|a3|Attended three (or more) meetings
        "A_approved": 7,  #7|ai|Inducted, needs to be notified
#       "A_dues_paid":8,  #8|ad|Inducted & notified, .....
#       "A_notified": 9,  #9|av|Vacancy pending payment of dues
#                         #10|aw|Inducted & notified, awaiting vacancy
#                         #11|am|New Member

        }
#       7|ai|Inducted, needs to be notified

def upgrade_applicant(applicant, date):
    """
    <applicant> must be a dict!
    We'll provide options to upgrade to a higher status
    such as adding a meeting.
    """
    print("Begin upgrade_applicant()")
    key2update = last_full_key(applicant)
    key2fill = first_empty_key(applicant)
    header = f"Data Entry ({key2fill[2:]})"
    helpers.print_header(header, bracket=True)
    print( f"""
          Updating {applicant["P_personID"]} 
          {applicant["P_first"]} {applicant["P_last"]}  
          {key2fill[2:]}
          """)
    new_date = input(f"Rtn to accept <{date}> or enter other date: ")
    if new_date: date = new_date
    q1 =f"""UPDATE Applicants SET {key2fill[2:]} = "{date}" WHERE
    personID = {applicant["P_personID"]};"""
    print()
    print(q1)
    print()
    q2 = f"""UPDATE Person_Status SET end = "{date}"
            WHERE personID = {applicant["P_personID"]}
            AND statusID = {key2status[key2update]}
            ;"""
    print(q2)
    print()
    q3 = f"""
            INSERT INTO Person_Status (personID, statusID, begin)
            VALUES ({applicant["P_personID"]}, 
                    {key2status[key2fill]},
                    "{date}")
        ;"""
    print(q3)
    print()

    # yet to implement entry into Receipts and possibly Dues owed

    yn = input("Go ahead with above 3 queries? (y/n) ")
    if yn and yn[0] in "yY":
        routines.fetch(q1, from_file=False, commit=True)
        routines.fetch(q2, from_file=False, commit=True)
        routines.fetch(q3, from_file=False, commit=True)

def add_meetings_cmd():
    date = helpers.eightdigitdate
    while True:
        yn = input("Credit applicant with a meeting? (y/n) ")
        if not (yn and yn[0] in 'yY'):
            return
        print()
        cur_apps = cur_app_dicts()
        app2update = applicant2update(cur_apps)
        if not app2update:
            continue
        upgrade_applicant(app2update, date)


if __name__ == "__main__":
    add_meetings_cmd()


