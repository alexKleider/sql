#!/usr/bin/env python3

# File: code/commands.py

"""

"""

import sqlite3
try:
    from code import routines
except ImportError:
    import routines

db_file_name = "Secret/club.db"


def get_command():
    choice = input("""Choose one of the following:
0. Exit
1. Show
2. Not implemented
...... """)
    if choice == '0': sys.exit()
    elif choice == '1': return show_cmd
    elif choice == '2': return appl_cmd
    elif choice == '3': print("Not implemented")
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
    return('\n'.join(report))


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
    return '\n'.join(report)


def for_angie():
    res = routines.fetch('Sql/forAngie.sql')
    report = []
    first_letter = 'A'
    for item in res:
        last_initial = item[1][:1]
        if last_initial != first_letter:
            first_letter = last_initial
            report.append("")
        report.append(
        "{1}, {0}".format(*item))
    return('\n'.join(report))


def show_cmd():
    members = show_members()
    applicants = show_applicants()
#   return members + "\n" + applicants
    return "\n".join((members, "\n", applicants))


if __name__ == "__main__":
    print(for_angie())
