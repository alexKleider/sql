#!/usr/bin/env python3

# File: code/commands.py

"""
Most of the code is here.
Driver of the code is main.py
"""

import sqlite3
import sys
import csv
try:
    from code import routines
except ImportError:
    import routines
try:
    from code import helpers
except ImportError:
    import helpers
try:
    from code import club
except ImportError:
    import club

def get_command():
    while True:
        choice = input("""Choose one of the following:
  0. Exit
  1. Show for web site
  2. Show applicants
  3. Show names as table
  4. Report
  5. yet2bNamed
  6. No email
  7. Get (non member) stati
  8. Update Status
  9. Find ID by name
 10. Populate Payables
 11. Update people demographics
 12. Add Dues
 13. Not implemented
...... """)
        if choice  ==   '0': sys.exit()
        elif choice ==  '1': return show_cmd
        elif choice ==  '2': return show_applicants
        elif choice ==  '3': return show_names
        elif choice ==  '4': return report_cmd
        elif choice ==  '5': return yet2bNamed
        elif choice ==  '6': return no_email_cmd
        elif choice ==  '7': return get_stati_cmd
        elif choice ==  '8': return update_status_cmd
        elif choice ==  '9': return id_by_name
        elif choice == '10': return populate_payables
        elif choice == '11': return update_people_cmd
        elif choice == '12': return add2dues_cmd
        elif choice == '13': return ["Not implemented", ]
        else: print("Not implemented")

# for add_dues:
# UPDATE table SET value = value + 5 WHERE id = 1;


def add2dues_cmd():
    """
    UPDATE Dues SET dues_owed = dues_owed + 100
    -- WHERE id = 1
    ;
    """
    # Add same to every entry since all are members.
    query = """
        UPDATE Dues SET dues_owed = dues_owed + 100;
        """
    con = sqlite3.connect(club.db_file_name)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return ['executed:', query]


def update_people_cmd():
    """
    """
    # whom to update?
    print("Whom to update?  ", end='')
    print('\n'.join(id_by_name()))
    personID = int(input("Enter your choice: "))

    # display data as it is currently:
    query = """SELECT * FROM People
        WHERE personID = ?;"""
    ret = routines.fetch(
            query,
#           db=club.db_file_name,
            params=(personID,),
            data=None,
            from_file=False,
            commit=False
            )
    ret = ret[0]
#   print(ret)
    original = [item for item in ret[1:]]
    ret = [item for item in ret[1:]]
    people_dict = {key: value for key, value in
            zip(club.people_keys, ret)}

    # provide user option to change values:
    while True:
        n = 1
        print("  0 to Quit")
        for key, value in people_dict.items():
            print(f"{n:>3}: {key}: {value}")
            n += 1
        response = int(input(
            "Enter index of field to change (or 0 to Quit:) "))
        if response == 0:
            break
        index = response - 1
        key = club.people_keys[index]
        new_value = input(f"Change {people_dict[key]} to: ")
        people_dict[key] = new_value
    sequence = [f"{key} = '{value}'" for key, value in
            people_dict.items()]
    for item in sequence:
        print(item)
    yes_no = input("Accept above values? (y/n): ")
    if yes_no and yes_no[0] in 'yY':
        values = ',\n'.join(sequence)
        query = """
            UPDATE People
            SET 
                {}
            WHERE
                personID = {};
        """.format(values, personID)
        print()
        print(query)
        response = input("OK to execute above query? (y/n) ")
        if response and response[0] in 'yY':
            con = sqlite3.connect(club.db_file_name)
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            ret = ['\nExecuted following query:',
                        query,
                        ]
        else:
            ret = ['Nothing done', ]
        return ret
    else: 
        print("not accepting new values")
        ret = ['Nothing done', ]


def populate_payables():
    """
    begin with a listing of all member IDs:
    for each of these, collect their dues and fees
        ==> a 'statement' for each ID
    For each of these, prepare either an email or letter
    File letters (into MailingDir) and
    store emails (=> emails.json)
    """
    query = """SELECT P.personID
            FROM 
                People AS P,
                Person_Status AS PS,
                Stati AS S
            WHERE
                PS.personID = P.personID 
            AND PS.statusID = S.statusID
            AND S.key = 'm'
            ;
    """
    ret = routines.fetch(
                query,
#               db=club.db_file_name,
                params=None,
                data=None,
                from_file=False,
                commit=False
                )
    memIDs = [str(entry[0]) for entry in ret]
    l = len(memIDs)
#   print(res)  # a list of all member IDs
#   res.append(f"There are {l} members")
    query4dues = """ -- add dues
    """
    query4dock = """ -- add docking fee
    """
    query4kayak = """  -- add kayak storage fee
    """
    query4mooring = """  -- add mooring fee
    """
    for memID in memIDs:  # currently listed as strings (not int)
        pass

    return res


def id_by_name():
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
    first = input("First name (partial or blank): ")
    last = input("Last name (partial or blank): ")
    params = [name+'%' if name else name for name in (first, last,)]
#   print(params)
    ret = routines.fetch(
                query,
#               db=club.db_file_name,
                params=params,
                data=None,
                from_file=False,
                commit=False
                )
    ret = ["{:3>} {} {} {}".format(*entry) for entry in ret]
#   _ = input(ret)
    return ret


def show_members():
    res = routines.fetch('Sql/show.sql')
#   first, last, suffix, phone, address, town, state, postal_code, email
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
"""{0} {1} {2} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item))
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
"""{first} {last} [{phone}] [{email}]
\t{address}, {town}, {state} {postal_code}
\tMeeting dates: {meeting_dates} 
\tSponsors: {sponsors}""".format(**d))
    return report


def for_angie(include_blanks=True):
    res = routines.fetch('Sql/forAngie.sql')
    report = []
    first_letter = 'A'
    for item in res:
        last_initial = item[1][:1]
        if ((last_initial != first_letter)
        and (include_blanks)):
            first_letter = last_initial
            report.append("")
        report.append(
        "{1}, {0}".format(*item))
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


def report_cmd():
    res = routines.fetch('Sql/show.sql')
    n = len(res)
    report = []
    helpers.add_header2list("Membership Report (prepared {})"
                            .format(helpers.date),
                            report, underline_char='=')
    report.append('')
    report.append('Club membership currently stands at {}.'
                  .format(n))
    report.extend(show_applicants())
    try:
        with open(club.ADDENDUM2REPORT_FILE, 'r') as fobj:
            addendum = fobj.read()
            if addendum:
                print('Appending addendum as found in file: {}'
                        .format(fobj.name))
                report.append("")
                report.append(addendum)
            else:
                print("No addendum found in file: {}"
                        .format(fobj.name))
    except FileNotFoundError:
        print('No addendum (file: {}) found.'
                .format(club.ADDENDUM2REPORT_FILE))
    report.extend(
        ['',
         "Respectfully submitted by...\n\n",
         "Alex Kleider, Membership Chair,",
         "for presentation to the Executive Committee on {}"
         .format(helpers.next_first_friday(exclude=True)),
         "(or at their next meeting, which ever comes first.)",
         ])
    report.extend(
        ['',
         'PS Zoom ID: 527 109 8273; Password: 999620',
        ])
    return report


def get_stati():
    """
    """
    con, cur = routines.initDB(club.db_file_name)
    res = routines.fetch(
            "Sql/get_non_member_stati.sql")
    # P.personID, P.first, P.last, St.key
    index = 0
    ret = {}
    for item in res:
        ret[index] = '{:>3}{:>10} {:<15} {}'.format(*item)
        ret[index] = item
        index += 1
    return ret


def get_stati_cmd():  # get_non_member_stati.sql
    """
    Returns a header followed by a listing of all
    people with a status OTHER THAN 'm':
    Use for presentation only.
    """
    res = get_stati()
    n = len(res)
    ret = [
#    13:  34     Angie Calpestri       z4_treasurer
     "People with non member stati (indexed)",
     " ##   ID     First Last            Status",
     "=========================================",
     ]
    for key in res.keys():
        # each item: P.personID, P.first, P.last, St.key
        entry = '{:>3}{:>10} {:<15} {}'.format(*res[key])
        ret.append(f'{key:>3}: {entry}')
    csv_file = input(
        "Name of csv file (return if not needed): ")
    if csv_file:
        print("Creation of csv not yet implemented.")
    return ret


def yet2bNamed():
    """
    John Maalis
    """
    ret = ["'yet2bNamed' still being implemented...", ]
    query = """SELECT St.key FROM 
        Stati AS St
        JOIN Person_Status AS PS
        ON PS.statusID = ST.statusID
        WHERE PS.personID = ?; """
    con = sqlite3.connect(club.db_file_name)
    cur = con.cursor()

    res = routines.get_ids_by_name(cur, con, 'John', 'Maalis')
    for personID in res:
        line = [str(personID)+':',]
        cur.execute(query, (personID,))
        stati = cur.fetchall()
#       _ = input(f"stati: {stati}") # stati: [('a3',)]
        line.extend([status[0] for status in stati])
        line = ' '.join(line)
        ret.append(line)
    _ = input(repr(ret))
    return ret


def no_email_cmd():
    """
    Provides a listing of _members_ without email.
    """
    con = sqlite3.connect(club.db_file_name)
    cur = con.cursor()
    for command in routines.get_commands("Sql/no_email.sql"):
        # only expect one command from this query
        cur.execute(command)
        res = cur.fetchall()
        n = len(res)
#       _ = input(res)
        ret = [
         "Member ID, Names and Demographics of {} without email"
         .format(n),
         "=====================================================",
         ]
        csv_file = input(
            "Name of csv file (return if not needed): ")
        if csv_file:
            fieldnames = ["personID", "first", "last",
                "address", "town", "state", "postal_code"]
            with open(csv_file, 'w', newline='') as outstream:
                writer = csv.DictWriter(outstream,
                        fieldnames=fieldnames)
                writer.writeheader()
                for line in res:
                    pairs = zip(fieldnames, line)
                    row = {}
                    for key, value in pairs:
                        row[key] = value
                    writer.writerow(row)
        for line in res:
            ret.append("{:>3}: {} {} {} {} {} {}".format(*line))
    return ret


def get_status_ID(status_key):
#   _ = input(status_key)
    status_id = routines.fetch(
            'Sql/get_status_id.sql',
            params=(status_key,))
#   _ = input(status_id)
    return status_id


def update_status_cmd():
    # First give user a look at what stati there are to change
    print('\n'.join(get_stati_cmd()))
    # ...Then present oportunity to pick a name not listed.
    names = input("Enter 'first last' if you need a personID: ")
    if names:
        names = names.split()
        ids_by_name = routines.get_ids_by_name(*names)
        for row in ids_by_name:
            print(row)
    personID = int(input("personID who's status to change: "))
    status2remove = input("Existing status to remove: ")
    status2add = input("New status: ")
#   _ = input("Entries are.." +
#       f"{personID}, {status2remove}, {status2add}")
    id2remove = id2add = ''
#   /* Sql/drop_person_status.sql *)
#   /* requires a 2 tuple (personID, statusID)
#   DELETE FROM Person_Status
#   WHERE personID = ? AND statusID = ?;
    ret = []
    if status2remove:
        id2remove = get_status_ID(status2remove,)
        id2remove = id2remove[0][0]
        res = routines.fetch(
                "Sql/drop_person_status.sql",
#DELETE FROM Person_Status
#WHERE personID = ? AND statusID = ?;
                params=(personID, id2remove, ),
                commit=True)
        _ = input(f"res: {res}")
        ret.append(f"Dropped ")
        
    if status2add:
        id2add = get_status_ID(status2add,)
        id2add = id2add[0][0]
        query = """ INSERT INTO Person_Status VALUES (?, ?) ;"""
        res = routines.fetch(query,
                params=(personID, id2add), from_file=False,
                commit=True)
    return [
            f"personID: '{personID}'",
            f"ID & key of status to remove: '{id2remove}'",
            f"ID & key of status to insert: '{id2add}'",
            ]


if __name__ == "__main__":
#   with open("4Angie.csv", 'w', newline='') as csvfile:
#       fieldnames = ('last', 'first')
#           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#           writer.writeheader()
#           for entry in for_angie():
#               writer.writerow(
#                   {'last': entry[0], 'first': entry[1]})
    print(for_angie())
