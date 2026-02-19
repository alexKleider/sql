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


def cur_app_dicts(query, from_file=False):
    """
    Returns a (possibly empty) listing of dicts:
    one for each applicant.
    """
    gen = routines.dicts_from_query(query,
                                    from_file=from_file,
                                    keys=None,
                                    replace_periods=True)
    return [dict(d) for d in gen]

def insert_new_applicant():
    """ NOT USED yet """
    pass

redact = '''
def current_applicants():
    """
    NOT USED
    Returns a (possibly empty) listing tuples:
    one for each applicant.
    """
    return routines.fetch(cur_applicants_query, from_file=True)
'''


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
    Returns users chosen applicant ID or
    None if none selected/available.
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
    ?unused
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

def keys2update2fill_tuple(applicant):
    """
    Returns a tuple of the keys of the last full
    and first empty value in the <applicant> dict.
    """
    key2update = None
    for key, val in applicant.items():
        if val:
            key2update = key[2:]
        else:
#           print(f"last_full_key returning {key}: {val}")
            return (key2update, key[2:])  #  key is the empty_key

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

def update_applicant(applicant, date):
    """
    <applicant> must be a dict!
    We'll provide options to upgrade to a higher status
    such as adding a meeting.
    Applicant table keys are: personID|sponsor1ID|sponsor2ID|
    app_rcvd|fee_rcvd|
    meeting1|meeting2|meeting3|
    approved|dues_paid|notified
    """
    print("Begin update_applicant()")
    key2update, key2fill = keys2update2fill_tuple(applicant)
    header = f"Data Entry ({key2fill})"
    helpers.print_header(header, bracket=True)
    print( f"""
          Updating {applicant["P_personID"]} 
          {applicant["P_first"]} {applicant["P_last"]}  
          {key2fill}
          """)
    new_date = input(f"Rtn to accept <{date}> or enter other date: ")
    if new_date: date = new_date
    q1 =f"""UPDATE Applicants SET {key2fill} = "{date}" WHERE
    personID = {applicant["P_personID"]};"""
    print()
    print(q1)
    print()
    q2 = f"""UPDATE Person_Status SET end = "{date}"
            WHERE personID = {applicant["P_personID"]}
            AND statusID = {key2update}
            ;"""
    print(q2)
    print()
    q3 = f"""
            INSERT INTO Person_Status (personID, statusID, begin)
            VALUES ({applicant["P_personID"]}, 
                    {key2fill},
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

def add_app_date_cmd():
    """
    Provides for addition of a date to the Applicant table
    and updated entries to the Person_Status table.
    """
    date = helpers.eightdigitdate
    while True:
        yn = input(
            "Add date to an entry in the Applicant table? (y/n) ")
        if not (yn and yn[0] in 'yY'):
            return
        print()
        cur_apps = cur_app_dicts("Sql/cur_applicants.sql",
                                 from_file=True)
        app2update = applicant2update(cur_apps)
        if not app2update:
            continue
        update_applicant(app2update, date)


if __name__ == "__main__":
    add_app_date_cmd()


