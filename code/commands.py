#!/usr/bin/env python3

# File: code/commands.py

"""
Most of the code is here.
Driver of the code is main.py
"""

import os
import sys
import csv
import shutil
import sqlite3
try: from code import routines
except ImportError: import routines

try: from code import helpers
except ImportError: import helpers

try: from code import club
except ImportError: import club

try: from code import content
except ImportError: import content

try: from code import alchemy
except ImportError: import alchemy

try: from code import dates
except ImportError: import dates

try: from code import fees
except ImportError: import fees

def get_command():
    while True:
        choice = input("""   MAIN MENU
Choose one of the following:
  0. Quit (or just return)      1. Show for web site
  2. Show applicants            3. Show names as table
  4. Report                     5. Send letter/email
  6. No email                   7. Get (non member) stati
  8. Update Status              9. Find ID by name
 10. Display Fees by person    11. Update demographics
 12. Data Entry (Dates)        13. Prepare Mailing
 14. Show Applicant Data       15. Add Meeting Date
 16. Display Fees by category  17. Welcome New Member
 18. Receipts                  19. Enter payments
 20. Create member csv file    21. Create applicant csv file
 22. Occupied moorings csv     23. All moorings csv
 24. Still owing csv           25. Membership < 1 year
 26. Fees (owing or not) csv   27. not implemented
...... """)
        if ((not choice) or (choice  ==   '0')): sys.exit()
        elif choice ==  '1': return show_cmd
        elif choice ==  '2': return show_applicants
        elif choice ==  '3': return show_names
        elif choice ==  '4': return report_cmd
        elif choice ==  '5': return send_cmd
        elif choice ==  '6': return no_email_cmd
        elif choice ==  '7': return get_stati_cmd
        elif choice ==  '8': return update_status_cmd
        elif choice ==  '9': return routines.id_by_name
        elif choice == '10': return display_fees_by_person_cmd
        elif choice == '11': return update_people_cmd
        elif choice == '12': return dates.date_entry_cmd
        elif choice == '13': return prepare_mailing_cmd
        elif choice == '14': return get_applicant_data_cmd
        elif choice == '15': return add_date_cmd
        elif choice == '16': return display_fees_by_category_cmd
        elif choice == '17': return welcome_new_member_cmd
        elif choice == '18': return receipts_cmd
        elif choice == '19': return payment_entry_cmd
        elif choice == '20': return create_member_csv_cmd
        elif choice == '21': return create_applicant_csv_cmd
        elif choice == '22': return occupied_moorings_cmd
        elif choice == '23': return all_moorings_cmd
        elif choice == '24': return still_owing_cmd
        elif choice == '25': return under1yr_cmd
        elif choice == '26': return fees.owing_csv_cmd
        else: print("Not implemented")

# for add_dues:
# UPDATE table SET value = value + 5 WHERE id = 1;

def not_implemented():
    return ["Not implemented", ]

def under1yr_cmd():
    ret = [
        "Creating list of members who's tenure is < 1 year...", ]
    with open("Sql/under1yr_f.sql", 'r') as stream:
        query = stream.read().format(
                        int(helpers.sixdigitdate)-10000)
    ret.append("Query is :")
    ret.extend(query.split("\n"))
    ret.append("...as far as we've gotten.")
    res = routines.fetch(query, from_file=False)
    for entry in res:
        ret.append(repr(entry))
    return ret


def still_owing_cmd():
    """
    """
    collector = []
    ret = ["Still owing csv being generated...", ]
    with open("Sql/memberIDs_f.sql", 'r') as stream:
        query = stream.read().format(helpers.sixdigitdate)
        # query orders by name...
    ret.append("query: ......")
    ret.extend(query.split('\n'))
    res = routines.fetch(query, from_file=False)
    for entry in res:
        data = routines.ret_statement(entry[0])
        if data['total'] == 0:
            continue
        data['ID'] = entry[0]
        data['first'] = entry[1]
        data['last'] = entry[2] + entry[3]
        collector.append(data)
    fieldnames = (
        "ID, first, last, total, dues, dock, kayak, mooring"
                                                .split(', '))
    csv_name = input("Name of csv file (owing.csv is default): ")
    if not csv_name: csv_name = "owing.csv"
    with open(csv_name, 'w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for data in collector:
            writer.writerow(data)
    ret.append("data writen to {csv_name}")
    return ret


def occupied_moorings_cmd():
    """
    Occupied moorings:  occupied_moorings_cmd
    Creates a csv file regarding occupied moorings.
    To be distinguished from all_moorings_cmd.
    """
    ret = ["Preparing a mooring CSV file...", ]
    fname = input("Enter name for csv file: ")
    if not fname:
        abort_message = (
                "No name, no results! Aborting execution")
        print(abort_message)
        ret.append(abort_message)
        return
    else:
        ret.append(f"You've chosen to create '{fname}'.")
    keys = ("personID, first, last, suffix, " +
            "mooring_code, cost, owing"
            ).split(', ')
    query = """
        SELECT P.personID, P.first, P.last, P.suffix,
            M.mooring_code, M.mooring_cost, M.owing
        FROM Moorings as M
        JOIN People as P
        WHERE P.personID = M.personID
        ;"""
    listing = routines.fetch(query, from_file=False)
    if not listing:
        ret.append("No results returned.")
        return
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for entry in listing:
            d = routines.make_dict(keys, entry)
            writer.writerow(d)
            ret.append(repr([row for row in d.items()]))
    ret.append(f"Sending mooring CSV file to {fname}.")
    return ret


def all_moorings_cmd():
    """
    All moorings: all_moorings_cmd
    Creates a csv file re all club moorings, occupied or not.
    To be distinguished from occupied_moorings_cmd.
    """
    ret = ["Preparing a mooring CSV file...", ]
    fname = input("\nEnter name for csv file: ")
    if not fname:
        abort_message = (
                "No name, no results! Aborting execution")
        print(abort_message)
        ret.append(abort_message)
        return
    else:
        ret.append(f"You've chosen to create '{fname}'.")
    query_keys = ("mooringID, mooring_code, " + 
            "mooring_cost, personID, owing")
    query = "SELECT {} FROM Moorings;".format(query_keys)
    listing = routines.fetch(query, 'Secret/club.db',
                from_file=False)
    if not listing:
        ret.append("No results returned.")
        return
    keys = ("mooring_ID", "code", "cost", "name", "owing")
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,
                fieldnames=keys)
        writer.writeheader()
        for entry in listing:
            rec = routines.make_dict(keys, entry)
            rec['name'] = routines.get_name(rec['name'])
#           ret.append(repr([row for row in rec.items()]))
            writer.writerow(rec)
    ret.append(f"Sending mooring CSV file to {fname}.")
    return ret


def update_people_cmd():
    """
    """
    # whom to update?
    print("Whom to update?  ", end='')
    print('\n'.join(routines.id_by_name()))
    personID = int(input("Enter your choice: "))

    # display data as it is currently:
    query = """SELECT * FROM People
        WHERE personID = ?;"""
    ret = routines.fetch(
            query,
#           db=club.DB,
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
            con = sqlite3.connect(club.DB)
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


def add2dues_cmd():
    """
    ###     FOR THE FUTURE     ###
    A one time only: add $100 to every one's dues.
    Taken off the menu.
    Will need to add entries for fees when year begins.
    Also will need to restrict the query to members only!!
    """
    return ['add2dues_cmd is a one time only!',
            'must not run it again!!!', ]
    query = """
        UPDATE Dues SET dues_owed = dues_owed + 200;
        """
    return['Following query _not_ executed:',
            query, ]
    con = sqlite3.connect(club.DB)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return ['executed:', query]


def get_fees_by_person(holder):
    """
    Sets up working_data attribute of holder.
    Same as assign_owing but without the dues.
    """
    byID = dict()
    # do dock privileges owing first:
    for tup in routines.fetch("Sql/dock1.sql"):
#       _ = input(tup)
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'dock': tup[4],
                }
    # add kayak storage owing:
    for tup in routines.fetch("Sql/kayak1.sql"):
        if tup[0] in byID.keys():
            byID[tup[0]]['kayak'] = tup[5]
        else:
            byID[tup[0]] = {'first': tup[1],
                            'last': tup[2],
                            'suffix': tup[3],
                            'kayak': tup[5],
                    }

    # and finally add mooring fee owing:
    for tup in routines.fetch("Sql/mooring1.sql"):
        if tup[0] in byID.keys():
            byID[tup[0]]['mooring'] = tup[5]
        else:
            byID[tup[0]] = {'first': tup[1],
                            'last': tup[2],
                            'suffix': tup[3],
                            'mooring': tup[5],
                    }
    # save what's been collected...
    holder.working_data = byID
#   for key, values in byID.items():
#       print(f"{key}: {values}")

def display_fees_by_person_cmd():
    """
    """
    ret = ['Extra fees being charged',
           '========================',
           ]
    holder = club.Holder()
    get_fees_by_person(holder)
    ret = []
    for person in holder.working_data.values():
        keys = [key for key in person.keys()]
#       _ = input(f"keys: {person.keys()}")
        if person['suffix']:
            entry = ["{first} {last},{suffix}:"
                            .format(**person), ]
        else:
            entry = ["{first} {last}:"
                            .format(**person), ]
        if 'dock' in keys:
            entry.append("  Dock usage fee .... ${:>3}"
                    .format(person['dock']))
        if 'kayak' in keys:
            entry.append("  Kayak storage fee . ${:>3}"
                    .format(person['kayak']))
        if 'mooring' in keys:
            entry.append("  Mooring fee ....... ${:>3}"
                    .format(person['mooring']))
        ret.extend(entry)
    return ret


def member_listing():
    """ 
    Returns a listing of the following values for each member:
    first, last, suffix, phone, address,
    town, state, postal_code, email
    """
    with open("Sql/show_f.sql", 'r') as infile:
        return routines.fetch(infile.read().format(
                                    helpers.sixdigitdate),
                        from_file=False)


def member_demo_dict(listing):
    """
    makes a dict from each listing as presented by member_listing
    """
    pass

def create_member_csv_cmd():
    csv_file_name = input("Name of member csv file to create: ")
    ret = [f"You've chosen to create '{csv_file_name}'.", ]
    keys = ("first, last, suffix, phone, address, " +
            "town, state, postal_code, email").split(", ")
    with open(csv_file_name, 'w', newline='') as csv_stream:
        writer = csv.DictWriter(csv_stream, fieldnames=keys)
        writer.writeheader()
        for listing in member_listing():
            writer.writerow(routines.make_dict(keys, listing))
    ret.append(f"Data sent to {csv_file_name}.")
    return ret


def show_members():
    res = member_listing()
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

def get_sponsor_name(sponsorID):
    query = f"""SELECT first, last, suffix
                FROM People 
                WHERE personID = {sponsorID}"""
    ret = routines.fetch(query, from_file=False)
    if not ret: return ''
    return ' '.join(ret[0]).strip()

app_keys = (
    "status_key, first, last, " +
    "phone, address, town, state, postal_code, email, " +
    "sponsor1ID, sponsor2ID, " +
    "app_rcvd, fee_rcvd, meeting1, meeting2, meeting3, " +
    "approved, dues_paid, Status_text").split(', ')

def applicant_listing():
    """
    Provides a listing of dicts (one for each applicant.)
    """
    listings = routines.fetch("Sql/applicants3.sql")
    ret = []
    for listing in listings:
        d = routines.make_dict(
                app_keys, [value for value in listing])
        d["sponsor1ID"] = get_sponsor_name(d['sponsor1ID'])
        d["sponsor2ID"] = get_sponsor_name(d['sponsor2ID'])
#       print(d)
        ret.append(d)
    return ret

def create_applicant_csv_cmd():
    ret = ["Preparing an applicant CSV file...", ]
    csv_file_name = input(
            "Name of applicant csv file to create: ")
    ret.append(f"You've chosen to create '{csv_file_name}'.")
    with open(csv_file_name, 'w', newline='') as csv_stream:
        writer = csv.DictWriter(csv_stream, fieldnames=app_keys)
        writer.writeheader()
        for d in applicant_listing():
            writer.writerow(d)
    ret.append(f"Sending applicant CSV file to {csv_file_name}.")
    return ret

def show_applicants():
    """
    query_file = 'Sql/applicants2.sql' ==>
    P.first, P.last, P.suffix,
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, inducted, dues_paid
    """
    headers = ('No meetings', 'Attended one meeting',    # 0, 1
        'Attended two meetings',                         # 2
        'Attended three (or more) meetings',             # 3
        'Approved (membership pending payment of dues)', # 4
        )
    # not sure the next two are being used!!
    date_keys = club.date_keys
    sponsor_keys = club.sponsor_keys
    
    res = routines.fetch('Sql/applicants2.sql')
    # convert our returned sequences into...
    dics = []        #  a sequence of dicts:
    for sequence in res:
        key_value_pairs = zip(club.appl_keys, sequence)
        mapping = {}
        for key, value in key_value_pairs:
            mapping[key] = value
#       _ = input(f"mapping: {mapping}")
        for sponsor in ('sponsor1', 'sponsor2'):
#           _ = input(f"sponsor: {mapping[sponsor]}")
            names = routines.fetch('Sql/find_1st_last_by_ID.sql',
                    params = (mapping[sponsor], ))[0]
#           _ = input(f"names: {names}")
            mapping[sponsor] = ' '.join(names).strip()
        dics.append(mapping)
    if not dics: print("NO SEQUENCE of DICTS")
    # Divide our sequence of dicts into a mapping
    # where keys are the headers and values are
    # lists of dicts to go under that header.
    header_mapping = {}
    for entry in dics:
        if entry['approved']:
            header_mapping.setdefault(headers[4], [])
            header_mapping[headers[4]].append(entry)
        elif entry['meeting3']:
            header_mapping.setdefault(headers[3], [])
            header_mapping[headers[3]].append(entry)
        elif entry['meeting2']:
            header_mapping.setdefault(headers[2], [])
            header_mapping[headers[2]].append(entry)
        elif entry['meeting1']:
            header_mapping.setdefault(headers[1], [])
            header_mapping[headers[1]].append(entry)
        elif entry['fee_rcvd']:
            header_mapping.setdefault(headers[0], [])
            header_mapping[headers[0]].append(entry)
#   _ = input(header_mapping)
    report = []  # header_mapping is a dict keyed by headers
            # and values are a list of (applicant) dicts
    for header in [header for header in headers
            if header in header_mapping.keys()]:
        report.append('\n'+header)
        report.append('-'*len(header))
        entry = []
        for mapping in header_mapping[header]:
            if mapping['approved']:
                entry.append(
                """{first} {last} {suffix} [{phone}] {email}
    {address}, {town}, {state} {postal_code}
    Sponsors: {sponsor1}, {sponsor2},
    Meetings: {meeting1} {meeting2} {meeting3}
    Date approved by Executive Committee: {approved}"""
                .format(**mapping))
            elif mapping['meeting1']:
                entry.append("""{first} {last} [{phone}] {email}
    {address}, {town}, {state} {postal_code}
    Sponsors: {sponsor1}, {sponsor2},
    Meetings: {meeting1} {meeting2} {meeting3} {approved}"""
                .format(**mapping))
            else:
                entry.append("""{first} {last} [{phone}] {email}
    {address}, {town}, {state} {postal_code}
    Sponsors: {sponsor1}, {sponsor2}"""
                .format(**mapping))
        report.extend(entry)
    return report


def for_angie(include_blanks=True):
    query = """
/* Sql/names_f.sql */
SELECT first, last
FROM People AS P
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati as St
ON St.statusID = PS.statusID
WHERE 
St.key IN ("m", "a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
AND (PS.end = 0 OR PS.end < {})
-- must insert today's date ^^ (helpers.todaysdate)
ORDER BY P.last, P.first
;
    """
    res = routines.fetch(
            query.format(helpers.sixdigitdate),
            from_file=False)
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
    applicant_header = 'Applicants'
    ret = show_members()
    ret.extend(('', '', applicant_header,
        '='*len(applicant_header), ))
    ret.extend(show_applicants())
    return ret


def show_names():
    return helpers.tabulate(
        for_angie(include_blanks=False),
        max_width=102, separator='  ')


def report_cmd():
    query = """
/* Sql/show_f.sql */
-- !! Requires formatting !!
-- retrieves member demographics
SELECT
    first, last, suffix, phone, address,
    town, state, postal_code, email
--    St.key, P.first, P.last
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
JOIN
    Stati as St
ON
    St.statusID = PS.statusID
WHERE 
    St.key = 'm'
    AND (PS.end = '' OR PS.end > {})
-- must format date membership ended or will end.
-- use code.helpers.sixdigitdate
ORDER BY
    P.last, P.first
;
    """
    res = routines.fetch(
            query.format(helpers.sixdigitdate),
            from_file=False)
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
    con, cur = routines.initDB(club.DB)
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


def get_stati_cmd(tocsv=True):  # get_non_member_stati.sql
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
    if tocsv:
        csv_file = input(
            "Name of csv file (return if not needed): ")
        if csv_file:
            with open(csv_file, 'w', newline='') as outf:
                writer = csv.DictWriter(outf,
                        fieldnames=('ID', 'first', 'last', 'status' ))
                writer.writeheader()
                for key in res.keys():
                    writer.writerow(
                            {'ID': res[key][0],
                             'first': res[key][1],
                             'last': res[key][2],
                             'status': res[key][3],
                             })
            print(f"Data written to '{csv_file}'.")
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
    con = sqlite3.connect(club.DB)
    cur = con.cursor()

#   res = routines.get_ids_by_name(cur, con, 'John', 'Maalis')
    res = routines.get_ids_by_name('John', 'Maalis')
    for personID in res:
#       _ = input(f"personID resolves to {personID}")
        line = [str(personID)+':',]
        cur.execute(query, (personID[0],))
        stati = cur.fetchall()
#       _ = input(f"stati: {stati}") # stati: [('a3',)]
        line.extend([status[0] for status in stati])
        line = ' '.join(line)
        ret.append(line)
#   _ = input(repr(ret))
    return ret


def no_email_cmd():
    """
    Provides a listing of _members_ without email.
    """
    con = sqlite3.connect(club.DB)
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
            ret.append("{:>3}: {} {}: {}, {}, {} {}".format(*line))
    return ret


def get_status_info(personID):
    """
    Returns ID, key, text for each status of personID
    eg: [(15, 'm', 'Member in good standing')]
    None if without status
    """
    ret = routines.fetch("Sql/get_stati_row_by_personID.sql",
            params=(personID,))
    return ret


def get_status_IDs(personID):
#   _ = input(status_key)
    status_ids = routines.fetch(
            'Sql/get_stati_by_personID.sql',
            params=(status_key,))
#   _ = input(status_id)
    return status_ids


def get_status_ID(status_key):
    """
    Returns the statusID of the status_key
    an invalid status_key causes return of NONE
    """
    ret = routines.fetch(
        "SELECT statusID from Stati WHERE key = ? ;",
        params=(status_key,), from_file=False)
    if ret:
        return ret[0][0]

_code_ = """
    while True:
        personID = input("Get row for ID (blank to quit): ")
        try:
            personID = int(personID)
        except ValueError:
            break
            """

def update_status_cmd():
    # First give user a look at what stati there are to change
    stati = get_stati_cmd(tocsv=False)
    print('\n'.join(stati))
    # ...Then present oportunity to pick a name not listed.
    yesorno = input("Do you need another person's ID? (y/n): ")
    if yesorno and yesorno[0] in 'yY':
        print('\n'.join(routines.id_by_name()))
    personID = int(input("personID who's status to change: "))
    personInfo = routines.fetch('Sql/find_by_ID.sql',
            params = (personID, ))[0]
    print(personInfo)
    # We've got a person, now show her stati:
    status2remove = input("Existing status to remove: ")
    status2add = input("New status: ")
    id2remove = id2add = ''
    ret = []
    if status2remove:
        id2remove = get_status_ID(status2remove,)
        print(f"id2remove set to {id2remove}")
    if status2add:
        id2add = get_status_ID(status2add,)
    params = (id2add, personID, id2remove)
    res = routines.fetch("Sql/changePersonStatus.sql",
            params = params, from_file=True,
            commit=True)
    return [
        f"personID: '{personID}'",
        f"person info: \n  {personInfo}",
        f"ID & key to remove: {id2remove}, '{status2remove}'",
        f"ID & key to insert: {id2add}, '{status2add}'",
            ]

def get_mailing_dict(personID):
    """
    Returns first, last, suffix,
    address, town, state, postal_code, country
    for personID
    """
    query_file = "Sql/get_mailing_dict.sql"
    return routines.fetch(query_file,
            params=(personID, )   )


def get_emailing_dict(personID):
    """
    Returns first, last, suffix, email
    for personID
    Empty list if no email.
    """
    query_file = "Sql/get_emailing_dict.sql"
    return routines.fetch(query_file,
            params=(personID, )   )


def assign_templates(holder):
    """ assign printer & templates..."""
    ret = ["Assigning printer & templates...",
           "within code.commands.assign_templates",]
    menu = routines.get_menu_dict(content.printers.keys())
    print("Printer to use...")
    for key, lpr in menu.items():
        print(f"{key}: {lpr}")
    index = int(input("Which printer to use? "))
    lpr = menu[index]
    ret.append(
        f"          for 'printer'.. {index:>3}: {lpr}")
    holder.lpr = content.printers[lpr]
    holder.letter_template = content.prepare_letter_template(
            holder.which,
            holder.lpr)
    holder.email_template = content.prepare_email_template(
            holder.which)
    return ret

def prepare_invoice(holder, personID):
    """
    holder.owed_by_id has already been assigned
    returns an iterable of strings that when '\n'.joined
    provides an invoice statement.
    """
    total = 0
    invoice = [f"Statement as of {helpers.today}:", ]
    for key, value in holder.owed_by_id[personID].items():
        invoice.append(f"    {key:<10} {value}")
        total += value
    invoice.append(f"        Total: ${total}")
    return invoice


def global_copies(holder):
#   if 'bcc' in list(data):
#       pass
#   if 'cc' in list(data):
#       if "sponsors" in list(data):
#           pass  # add sponsor emails
    return(['Dealing with cc and bcc.', ])


def sponsor_copies(holder, data):
    pass


def prepare_mailing_cmd():
    """
    ck for 'cc', especially in response to 'sponsors'
    & assign holder.cc if needed
    insert checks regarding mail dir and email.json
    then set up mailing dir and holder.emails (a
                             list of dicts for emails)
    Traverse records applying funcs
      populating holder.mail_dir and holder.email list
    Move holder.email listing into a json file (if not empty.)
    Delete mail_dir if it's empty
    """
    holder = club.Holder()
    ret = []
    # give user opportunity to abort if files are still present:
    print("Checking for left over files (must be deleted!) ...")
    helpers.check_before_deletion((holder.email_json,
                                    holder.mail_dir),
                                    delete=True)
    os.mkdir(holder.mail_dir)
    response = routines.get_menu_response(content.ctypes)
    if response == 0:
        ret.append("Quiting per your choice")
        return ret
    w_key = content.ctypes[response-1]  # which_key
    ret = [
        f"Your choice for 'w_key'.. {response:>3}: {w_key}", ]
    holder.which = content.content_types[w_key]
    # which letter has been established & conveyed to the holder
    # now: establish printer to be used and assign templates
    ret.extend(assign_templates(holder))
    # find out if we need to cc or bcc anyone:
    which_keys = set(holder.which.keys())
    if which_keys and {'cc', 'bcc'}:
        ret.extend(global_copies(holder))

    holder.emails = []
    for func in holder.which['holder_funcs']:
        # assigns holder.working_data
        # will probably end up only needing one 
        # for billing: routines.assign_owing   <<<<
        func(holder)
#       ret.extend(func(holder))
    for dic in holder.working_data.values():
        for func in holder.which['funcs']:  #  vvvvv
            # for billing: members.send_statement(holder, dic)
#           ret.extend(func(holder, dic))
            func(holder, dic)
    # send holder.emails to a json file
    helpers.dump2json_file(holder.emails, holder.email_json)
    # Delete mailing dir if no letters are filed:
    if os.path.isdir(holder.mail_dir) and not len(
            os.listdir(holder.mail_dir)):
        os.rmdir(holder.mail_dir)
        print("Empty mailing directory deleted.")
    else:
        print("""..next step might be the following:
    $ zip -r 4Peter {0:}
    (... or using tar:
    $ tar -vczf 4Peter.tar.gz {0:}"""
            .format(holder.mail_dir))
    print("prepare_mailing completed..")
    return ret


def show_applicant_data(ID):
    ret = routines.fetch('Sql/show_applicant_data4ID.sql',
            params=(ID,))
    print("returning ...")
    print(ret)
    ret = [line for line in ret]
    if len(ret) > 1:
        print(f"Only first line being shown for {ID}")
    return ret[0]


def get_applicant_data_cmd():
    response = input("Enter ID, blank for prompt: ")
    if not response:
        ret = routines.id_by_name()
        for line in ret:
            print(line)
    appID = input("Enter ID: ")
    if not appID:
        print("Lack of entry ==> termination!")
        sys.exit()
    return show_applicant_data(appID)


def send_cmd():
    ret = ['mailing command is under development', ]
    okrange = range(1,len(content.ctypes)+1)
    choices = zip(okrange, content.ctypes)
    print("""   MAILING MENU
Choose a mailing type from one of the following:""")
    for choice in choices:  # prints the menu..
        print(f'{choice[0]:<3}: {choice[1]}')
    response = int(input("Choice ('0' to quit): "))
    _ = input(f"You chose '{content.ctypes[response-1]}'")
    return ret


def add_date_cmd():
    ret = ['Adding to applicant dates...']
    # get a personID of the person who's data to modify
    print("Choose from the following...")
    for line in routines.id_by_name():
        print(line)
    personID = int(input(
        "Pick a personID (must be an integer): "))
    # get which date key to modify (provides formatting)
    menu = routines.get_menu_dict(club.date_keys)
    while True:
        print("Choices:")
        for key, entry in menu.items():
            print(f'{key}: {entry}')
        n = int(input("Enter # of date key to modify: "))
        if n in menu.keys():
            date_key = n
            break
    # get date to insert (over write!)
    while True:
        date = input(
            "Date (6 digits in 'yymmdd' format) to insert: ")
        confirm = input(f"Is {date} correct? (y/n): ")
        if confirm and confirm[0] in 'yY':
            break
    query = """/* Sql/set_date.sql */
    UPDATE Applicants
    SET {0:} = :{0:} 
    WHERE personID = :personID
    ;
    """
    query = query.format(*(menu[date_key], ))
    params = {f'{date_key}': f'{date}',
        'personID': f'{personID}',
        }
    print(query)
    print(params)
    nogood = "{'4': '230330', 'personID': '<built-in function id>'}"
    ret.append(query)
    ret.append(repr(params))
    r = input("Continue? (y/n): ")
    if r and r[0] in 'yY': 
        alchemy.alch(query, dic=params, from_file=False) 
    else:
        ret.append('Aborting...')
    return ret

def name_from_tup(tup):
    if tup[3]:
        name = "{1} {2}{3}".format(*tup)
    else:
        name = "{1} {2}".format(*tup)
    return name


def display_fees_by_category_cmd():
    ret = ['Special Fees Being Charged',
           '==========================',
           ]
    dock = ['Dock Usage ($75)',
            '----------------',
            ]
    kayak = ['Kayak Storage /w Slot# ($100)',
             '----------------------------',
             ]
    mooring = ['  Mooring Location & Cost',
               '( U)pper, M)iddle and S)tring )',
               '  ---------------------------',
               ]
    for tup in routines.fetch("Sql/dock1.sql"):
        dock.append(f"  {name_from_tup(tup)}")
    for tup in routines.fetch("Sql/kayak1.sql"):
        kayak.append(f"  {tup[4]} {name_from_tup(tup)}")
    for tup in routines.fetch("Sql/mooring1.sql"):
        mooring.append(
                f"  {tup[4]} @ ${tup[5]} {name_from_tup(tup)}")
    ret.extend(dock)
    ret.append('')
    ret.extend(kayak)
    ret.append('')
    ret.extend(mooring)
    return ret

def welcome_new_member_cmd():
    ret = ['<welcome_new_member_cmd>',
            ]
    print("Create list of people to welcome as new member(s):")
    candidates = []
    while True:
        ids = routines.id_by_name()
        if not ids:
            break
        print('\n'.join(ids))
        print(f"Enter (coma separated if > 1) list of IDs:")
        response = input("Listing of IDs or blank to quit: ")
        if not response:
            break
        else:
            _ = input(f"Your response: {response}")
            candidates.extend([int(entry) for entry in
                                response.split(",")])
    if not candidates:  # nothing to do
        ret.append("No candidate(s) specified. Nothing to do.")
        return ret
    _ = input(f"Entries: {candidates}")
    ret.append('You chose the following: ' + ', '.join(
            [str(candidate) for candidate in candidates]))
    return ret

def receipts_cmd():
    list_of_dicts = []
    fields = ("personID date_received dues dock kayak "
            + "mooring acknowledged")
    keys = fields.split()
    fields = ', '.join(keys)
    query = (f"SELECT {fields}  FROM Receipts;")
#   ret.append(query)
    report = [f"Receipts for {helpers.this_year} ...", 
        "Name   payment date, fees, dock, kayak, mooring,  date acknowledged",
            ]
    for res in routines.fetch(query, from_file=False):
        data = {}
        for n in range(len(keys)):
            data[keys[n]] = res[n]
        names = routines.get_person_fields_by_ID(
                    data['personID'],
                    fields = ("first last suffix".split())  )
#       _ = input(repr(names))
        data['personID'] = "{first} {last}{suffix}".format(**names)
        line = ''.join((
                "{personID:<17} {date_received:>10} {dues:>5},",
                "{dock:>5}, {kayak:>5}, {mooring:>5},",
                "{acknowledged:>10}", ))
        line = line.format(**data)
        report.append(line)
        list_of_dicts.append(data)
    response = input(
        "Create csv file? (enter a name or leave blank)... ")
    if response:
        helpers.save_db(list_of_dicts, response, data.keys(),
                report="receipts")
    return report


def payment_entry_cmd():
    ret = ['Entering payment_entry_cmd...', ]
    ret.append('For payment entry use 12. Data Entry (Dates)')
    print(ret[0])
    return(ret)


if __name__ == "__main__":
#   for sponsor_name in (get_sponsor_name(45),
#           get_sponsor_name(300)):
#       print(repr(sponsor_name))
    applicant_listing()
#   with open("4Angie.csv", 'w', newline='') as csvfile:
#       fieldnames = ('last', 'first')
#           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#           writer.writeheader()
#           for entry in for_angie():
#               writer.writerow(
#                   {'last': entry[0], 'first': entry[1]})
#   print(for_angie())
#   try_applicants()
#   print(get_emailing_dict(101))
