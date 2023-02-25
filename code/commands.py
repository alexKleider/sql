#!/usr/bin/env python3

# File: code/commands.py

"""

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

db_file_name = "Secret/club.db"
ADDENDUM2REPORT_FILE = "Secret/addendum2report.txt"

def get_command():
    choice = input("""Choose one of the following:
 0. Exit
 1. Show for web site
 2. Show applicants
 3. Show names as table
 4. Report
 5. yet2bNamed
 6. No email
 7. Get stati
 8. Update Status
 9. Not implemented
...... """)
    if choice == '0': sys.exit()
    elif choice == '1': return show_cmd
    elif choice == '2': return show_applicants
    elif choice == '3': return show_names
    elif choice == '4': return report_cmd
    elif choice == '5': return yet2bNamed
    elif choice == '6': return no_email_cmd
    elif choice == '7': return get_stati_cmd
    elif choice == '8': return update_status_cmd
    elif choice == '9': print("Not implemented")
    else: print("Not implemented")


def show_members():
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
"""{first}, {last} [{phone}] {address}, {town}, {state} {postal_code} [{email}]
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
        with open(ADDENDUM2REPORT_FILE, 'r') as fobj:
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
                .format(ADDENDUM2REPORT_FILE))
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


def get_stati_cmd():
    """
    personID, status2remove, status2add
    """
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    for command in routines.get_commands("Sql/get_non_member_stati.sql"):
        # only expect one command from this query
        cur.execute(command)
        res = cur.fetchall()
        n = len(res)
        ret = [
         "People with special (other than member) stati",
         "=============================================",
         ]
        for item in res:
            ret.append('{:>3}{:>10} {:<15} {}'.format(*item))
        return ret
        csv_file = input(
            "Name of csv file (return if not needed): ")


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
    con = sqlite3.connect(db_file_name)
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
    con = sqlite3.connect(db_file_name)
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


def get_status_key(status):
    query = f"""SELECT    statusID, key
                FROM Stati
                WHERE key = '{status}'"""
    ret = routines.connect_and_get_data(query)


def update_status_cmd():
    personID = input("personID who's status to change: ")
    status2remove = input("Existing status to remove: ")
    status2add = input("New status: ")
    _ = input("Entries are.." +
        f"{personID}, {status2remove}, {status2add}")
    key2remove = get_status_key(status2remove)
    key2add = get_status_key(status2add)
    return ['Not yet implemented',
            f"personID: '{personID}'",
            f"key to remove: '{key2remove}'",
            f"key to insert: '{key2add}'",
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
