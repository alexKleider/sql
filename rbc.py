#!/usr/bin/env python3

# File: rbc.py    ... driver for club data base

# Author: Alex Kleider
# Code modeled after that of A J Gauld
# @ http://www.alan-g.me.uk/l2p2/index.htm
#  ... "working with databses"
"""
"""

# set up the database and cursor
import sys
import sqlite3
from code import club
from code import routines

dbpath = "/home/alex/Git/Sql/Secret/"
club_db = "club.db"

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

# commands

def id_by_name(cursor):
    """
    Prompts for first letter(s) of first &/or last
    name(s) and returns a listing of matching entries
    from the 'People' table (together with IDs.)
    If both are blank, none will be returned!
    """
    query = """
    SELECT personID, first, last, suffix
    FROM People
    WHERE first LIKE ? OR last LIKE ? 
    ;
    """
    print("Looking for people:")
    print("Narrow the search, use * to eliminate a blank...")
    first = input("First name (partial, blank or '*'): ")
    last = input("Last name (partial, blank or '*'): ")
    params = [
        name+'%' if name else name for name in (first, last,)]
#   print(params)
    cursor.execute(query, params)
    ret = cursor.fetchall()
    ret = ["{:3>} {} {} {}".format(*entry) for entry in ret]
#   _ = input(ret)
    return ret


def show_members():
    query = """ SELECT first, last, phone,
        address, town, state, postal_code, email
        --    St.key, P.first, P.last
        FROM People AS P
        JOIN Person_Status AS PS
        ON P.personID = PS.personID
        JOIN Stati as St
        ON St.statusID = PS.statusID
        WHERE St.key = 'm'
        ORDER BY P.last, P.first
        ; """
    res = routines.fetch('Sql/show.sql')
    n = len(res)
#   _ = input(f"Number of members: {n}\n")
    report = [f"""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS ROD &
BOAT CLUB MEMBERSHIP CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED
FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BOARD OF THE BRBC.

There are currently {n} members in good standing:
""", ]
    first_letter = 'A'
    for item in res:
        last_initial = item[1][:1]
        if last_initial != first_letter:
            first_letter = last_initial
            report.append("")
        report.append(
        "{}, {} [{}] {}, {}, {} {} [{}]".format(*item))
    return report


def show_applicants():
    """
('a0', 'Sandra', 'Buckley', '707/363-0754', '10 Canyon Rd. #57', 'Bolinas', 'CA', '94924-0057', 'sandrabuckley@att.net', 'Billy Cummings', 'Sandy Monteko-Sherman', '221221', '221221', '', '', '', '', '', '', 'Applicant (no meetings yet)')
    """
    keys = (
    'St_key', 'first', 'last', 
    'phone', 'address', 'town', 'state', 'postal_code', 'email',
    'sponsor1', 'sponsor2',
    'app_rcvd', 'fee_rcvd', 'meeting1', 'meeting2', 'meeting3',
    'approved', 'inducted', 'dues_paid', 'St_text',)
    meeting_keys = ('meeting1', 'meeting2', 'meeting3',)
    sponsor_keys = ('sponsor1', 'sponsor2',)
    res = routines.fetch('Sql/applicants.sql')
    n = len(res)
    report = [
        f"There are currently {n} applicants.",
         "===================================",
         ]
    header = ''
    for entry in res:
        d = routines.make_dict(keys, entry)
        meeting_dates = [d[k] for k in meeting_keys if d[k]]
        if not meeting_dates:
            d['meeting_dates'] = 'no meetings yet'
        else:
            d['meeting_dates'] = ', '.join(meeting_dates)
        sponsors = [d[k] for k in sponsor_keys if d[k]]
        if not sponsors:
            d['sponsors'] = 'not available'
        else:
            d['sponsors'] = ', '.join(sponsors)
        if d['St_text'] != header:
            header = d['St_text']
            report.extend(['', header, '-' * len(header)])
        report.append(
"""{first} {last} [{phone}] {address}, {town}, {state} {postal_code} [{email}]
\tMeeting dates: {meeting_dates} 
\tSponsors: {sponsors}""".format(**d))
    return report
def show_cmd():
    members = show_members()
    applicants = show_applicants()
#   return members + "\n" + applicants
    return members + ["\n"] + applicants


def show_names():
    return helpers.tabulate(
        for_angie(include_blanks=False),
        max_width=102, separator='  ')


# Driver functions
def addEntry(book):
    first = input('First name: ') 
    last =  input('Last name: ') 
    house = input('House number: ') 
    street = input('Street name: ') 
    district = input('District name: ') 
    town =  input('City name: ') 
    code =  input('Postal Code: ') 
    phone = input('Phone Number: ') 
    query = '''INSERT INTO Address 
               (First,Last,House,Street,District,Town,PostCode,Phone)
               VALUES (?,?,?,?,?,?,?,?)'''
               
    try:
       book.execute(query,(first, last, house, street, district, town, code, phone))
    except sqlite3.OperationalError:  
       print( "Insert failed" )
       raise
    return None

def removeEntry(book):
    name  = input("Enter a name: ")
    names = name.split()
    first = names[0]; last = names[-1]
    try:
       book.execute('''DELETE FROM Address 
                    WHERE First LIKE ? 
                    AND Last LIKE ?''',(first,last))
    except sqlite3.OperationalError: 
       print( "Remove failed" )
       raise
    return None

def get_sponsor_ids(theClub):
    print("Finding sponsor IDs")
    sponsorIDs = []
    while len(sponsorIDs) < 2:
        print('\n'.join(id_by_name(theClub)))
        id = input("Enter sponsor's ID: ")
        if id: sponsorIDs.append(id)
    return sponsorIDs


def addNewApplicant(theClub):
    ## collect applicant's demographics:
    ret = ['Within addNewApplicant',]
    print("provide entries for each of the following:")
    entries = dict()
    for key in club.people_keys:
        entries[key] = input(f"{key}: ")
    while True:
        key = input(
          "Enter key of field to fix or hit <Enter> if all OK: ")
        if not key: break
        if not (key in club.people_keys):
            print(f"'{key}' is an invalid key.")
            continue
        entries[key] = input(f"{key}: ")
    table = 'People'
    print(f"table: {table}")
    keys = ', '.join([key for key in entries.keys()])
    print(f"keys: {keys}")
    values = ', '.join(
            [f'"{value}"' for value in entries.values()])
    print(f"values: {values}")

    ## send applicant demographics to People table
    query = """INSERT INTO {table} ({keys})
                VALUES({values});""".format(
                    table='People',
                    keys=keys,
                    values=values)
    try:
        theClub.execute(query)
        result = theClub.fetchall()
#       for entry in result:
#           print(repr(entry))
    except sqlite3.OperationalError: 
       print(
       "Sorry, new applicant insertion into People table failed")
       raise
    else:
        if result:
           for line in result:
               ret.append( repr(line) )
        else: ret.append("Nothing returned after insersion.")

    ## retrieve the personID of the entry just made.
    query = """
    SELECT personID FROM People WHERE
    first = ? AND last = ? AND suffix = ? ;
    """
    params = [entries[key] for key in ('first', 'last', 'suffix')]
    try:
        theClub.execute(query, params)
        result = theClub.fetchall()
#       for entry in result:
#           print(repr(entry))
    except sqlite3.OperationalError: 
       ret.append( "Sorry search for personID failed" )
       raise
    else:
        if result:
            personID = result[0][0]
            print(f"'personId' of new entry is {personID}")
#           for line in result:
#               ret.append( repr(line) )
        else: ret.append("personID not retrieved.")

    ## collect sponsors and get their IDs
    sponsorIDs = get_sponsor_ids(theClub)
    ret.append("sponsor ids are: {} & {}"
                    .format(*sponsorIDs))

    ## Setup:
    keys = ('sponsor1', 'sponsor2',
            'app_rcvd', 'fee_rcvd',
            'meeting1', 'meeting2', 'meeting3',
            'inducted', 'dues_paid')
    headers = ['personID', ]
    ap_data = [str(personID), ]
    for index in range(2):
        headers.append[keys[index]]
        ap_data.append('"{}"'.format(sponsorIDs[index]))

    # collect dates
    for key in keys[2:]:
        date = input(f"{key}: ")
        if not date: break
        headers.append(key)
        ap_data.append('"{}"'.format(str(date)))

    ## Add entry to Applicants table
    query =  """
    INSERT INTO Applicants ({})
        VALUES ({})
       ;""".format(', '.join(headers), ', '.join(ap_data))
    try:
        theClub.execute(query)
        result = theClub.fetchall()
#       for entry in result:
#           print(repr(entry))
    except sqlite3.OperationalError: 
       print( "Sorry Applicants table insertion failed" )
       raise
    else:
        if result:
           for line in result:
               ret.append( repr(line) )
        else: ret.append(
            "Nothing returned after Applicant table insersion.")

    return ret


def updateApplicant(theClub):
    """
    Use each time an applicant's status changes.
    """
    print("Look for applicants personID...")
    choices = findPerson(theClub)
    for choice in findPerson(theClub):
        print(choice)
    personID = input("personID of applicant to update: ")
    print(personID)
    ret = [f"personID of applicant is {personID}", ]
    
def findPerson(theClub):
    """
    Working under new system.
    """
    ret = []
    fieldnames = ["personID", "first", "last",
        "address", "town", "state", "postal_code"]
    field = input("Enter a search field: ")
    value = input("Enter a search value: ")
    value = value + '%'
    if field in fieldnames:
        query = f"""SELECT personID, first, last, suffix,
                address, town, state, postal_code 
            FROM People WHERE {field} LIKE ?;"""
    else: raise ValueError("invalid field name")
    try:
        theClub.execute(query, (value,) )
        result = theClub.fetchall()
#       for entry in result:
#           print(repr(entry))
    except sqlite3.OperationalError: 
       ret.append( "Sorry search failed" )
       raise
    else:
        if result:
           for line in result:
               ret.append( repr(line) )
        else: ret.append("No matching data")
    return ret


def testDB(database):
    database.execute("SELECT * FROM Address")
    print( database.fetchall() )
    return None

def closeDB(database, cursor):
    try:
       cursor.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise
       
# User Interface functions
def getChoice(menu):
    print( menu )
    choice = input("Select a choice(0-...): ")
    return choice


def main():
    theMenu = """
      0. Exit
      1. Show for web site
      2. Show applicants
      3. Show names as table
      4. Report
      5. yet2bNamed
      6. No email
      7. Get stati
      8. Update Status
      9. Find ID by name
     10. Populate Payables
     11. Update people demographics
     12. Add Dues
     13. Not implemented
     22. Find person
     33. Add new applicant
     44. Search for an ID
     55. Get sponsor IDs
     66. Update applicant
     99. Quit and save
    ...... """

    try:
        theDB, theClub = initDB(dbpath + club_db)
        while True:
            ret = ["No results",]
            choice = getChoice(theMenu)
            if choice == '0': break
            if choice == '99': break
            if choice == '1': show_cmd(theClub)
            elif choice == '2' or choice.upper() == 'R':
               removeEntry(theClub)
            elif choice == '3' or choice.upper() == 'F':
               try: findEntry(theClub)
               except: ValueError: print("No such field name")
            elif choice == '4' or choice.upper() == 'T':
               testDB(theClub)
            elif choice == '22': ret = findPerson(theClub)
            elif choice == '33': ret = addNewApplicant(theClub)
            elif choice == '44': ret = id_by_name(theClub)
            elif choice == '55': ret = get_sponsor_ids(theClub)
            elif choice == '66': ret = updateApplicant(theClub)
            else: print( "Invalid choice, try again" )
            if not ret: print("No results from Menu")
            else:
                response = input(
                    "Send to file? (blank if to stdout): ")
                if response:
                    with open(response, 'w') as outf:
                        outf.write('\n'.join(response))
                else:
                    _ = input('\n'.join(ret))

    except sqlite3.OperationalError:
        print(
        "Database error raised in <main>, exiting program.")
        # raise
    finally: 
        closeDB(theDB,theClub)

# for add_dues:
# UPDATE table SET value = value + 5 WHERE id = 1;
    
def old_main():
    theMenu = '''
    1) Add Entry
    2) Remove Entry
    3) Find Entry
    4) Test database connection
    
    9) Quit and save
    '''
    
    try:
       theDB, theClub = initDB(dbpath + club_db)
       while True:
           choice = getChoice(theMenu)
           if choice == '9' or choice.upper() == 'Q':
              break
           if choice == '1' or choice.upper() == 'A':
               addEntry(theClub)
           elif choice == '2' or choice.upper() == 'R':
               removeEntry(theClub)
           elif choice == '3' or choice.upper() == 'F':
               try: findEntry(theClub)
               except: ValueError: print("No such field name")
           elif choice == '4' or choice.upper() == 'T':
               testDB(theClub)
           else: print( "Invalid choice, try again" )

    except sqlite3.OperationalError:
        print( "Database error, exiting program." )
        # raise
    finally: 
        closeDB(theDB,theClub)

if __name__ == '__main__':
#   # verify data base
#   response = input(
#       f"OK to use {dbpath + club_db} as data base?")
#   if not (response and response[0] in 'yY'):
#       sys.exit()

    main()


