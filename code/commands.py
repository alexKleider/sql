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

try: from code import applicants
except ImportError: import applicants

try: from code import show
except ImportError: import show


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
 26. Fees (owing or not) csv   27. Enter applicant data
 28. Show stati
...... """)
        if ((not choice) or (choice  ==   '0')): sys.exit()
        elif choice ==  '1': return show.show_cmd
        elif choice ==  '2': return show_applicants
        elif choice ==  '3': return show_names
        elif choice ==  '4': return report_cmd
        elif choice ==  '5': return send_cmd
        elif choice ==  '6': return no_email_cmd
        elif choice ==  '7': return get_non_member_stati_cmd
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
        elif choice == '27':
            return applicants.applicant_data_entry_cmd
        elif choice == '28': return show_stati_cmd
        else: print("Not implemented")

# for add_dues:
# UPDATE table SET value = value + 5 WHERE id = 1;

def send_cmd():
    """
    Should be redacted!
    Use ./send_emails.py
    """
    ret = [
      "Send email functionality is not available from this menu.",
      "Use './send_emails.py' instead.",
      ]
    for line in ret:
        print(line)
    return ret

def payment_entry_cmd():
    """
    Redact- not used.
    """
    ret = ['"payment_entry_cmd" has been redacted.',
            'For payment entry use 12. Data Entry (Dates)',
            ]
    for line in ret: print(line)
    return(ret)

def not_implemented():
    return ["Not implemented", ]

def under1yr_cmd():
    under1yr_file_name = "Secret/under1yr.csv"
    text = ["Members of <1 Year",
                ]
    text.append("=" * len(text[0]))
    ret = [
        "Creating list of members who's tenure is < 1 year...", ]
    query = routines.import_query("Sql/under1yr_ff.sql").format(
            int(helpers.eightdigitdate)-10000,
            helpers.eightdigitdate,
            int(helpers.eightdigitdate)-10000)
    keys = (("personID, first, last, " +
            "suffix, text, begin, end").split(', '))
    ret.append("Query is :")
    ret.extend(query.split("\n"))
    res = routines.fetch(query, from_file=False)
    data = [helpers.make_dict(keys, item) for item in res]
    for entry in res:
        ret.append(repr(entry))
    for datum in data:
        ret.append(repr(datum))
        text.append(repr(datum))
    ret.append("Listing of members <1yr being sent to " +
           f"{under1yr_file_name}")
    print(ret[-1])
    with open(under1yr_file_name, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=keys)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    return ret


def still_owing_cmd():
    """
    Note: suffix is appended to last if it exists.
    """
    output_file_name = "Secret/owing.csv"
    collector = []
    ret = ["Still owing csv being generated...", ]
    with open("Sql/memberIDs_f.sql", 'r') as stream:
        query = stream.read().format(helpers.eightdigitdate)
        # query orders by name...
    ret.append("query: ......")
    ret.extend(query.split('\n'))
    res = routines.fetch(query, from_file=False)
    for entry in res:
        data = routines.ret_statement(entry[0])
        if data['total'] <= 0:
            continue
        data['ID'] = entry[0]
        data['first'] = entry[1]
        data['last'] = entry[2] + entry[3]
        collector.append(data)
    fieldnames = (
        "ID, first, last, total, dues, dock, kayak, mooring"
                                                .split(', '))
    print(f"Default output file is {output_file_name}")
    csv_name = input(
        "Enter a different name or leave blank for defauld: ")
    if not csv_name: csv_name = output_file_name
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
            d = helpers.make_dict(keys, entry)
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
            rec = helpers.make_dict(keys, entry)
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
            writer.writerow(helpers.make_dict(keys, listing))
    ret.append(f"Data sent to {csv_file_name}.")
    return ret


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
        d = helpers.make_dict(
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


def for_angie(include_blanks=True):
    """
    Returns a table of member and applicant names.
    """
    query = """
/* Sql/names_f.sql */
SELECT first, last, suffix
FROM People AS P
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati as St
ON St.statusID = PS.statusID
WHERE 
St.key IN ("m", "a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
AND (PS.end = '' OR PS.end > {})
-- must insert today's date ^^ (helpers.todaysdate)
ORDER BY P.last, P.first, P.suffix
;
    """
    keys = "first, last, suffix".split(', ')
    report = ['', ]
    first_letter = 'A'
    for d in routines.query2dict_listing(
            query.format(helpers.eightdigitdate),
            keys, from_file=False):
        if ((d['last'][:1] != first_letter)
        and (include_blanks)):
            first_letter = d['last'][:1]
            report.append("")
        if d['suffix']:
            fstring = "{last}, {first} ({suffix})"
        else: fstring = "{last}, {first}"
        submission = fstring.format(**d)
        if submission != report[-1]:
            report.append(submission)
    return report[1:]

# see "redacted" file

def show_names():
    return helpers.tabulate(
        for_angie(include_blanks=False),
        max_width=102, separator='  ')


def report_cmd():
    outfile = f"report{helpers.eightdigitdate}.txt"
    n = len(show.member_listing())
    report = []
    helpers.add_header2list("Membership Report (prepared {})"
                            .format(helpers.date),
                            report, underline_char='=')
    report.append('')
    report.append('Club membership currently stands at {}.\n'
                  .format(n))
    report.extend(show.show_applicants_cmd())
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
    print(f"Default file name is '{outfile}'...")
    response = input("Blank to accept or enter new name: ")
    if response:
        outfile = response
    with open(outfile, 'w') as outf:
        outf.write('\n'.join(report))
    return report


def get_non_member_stati():
    """
    """
    keys = ("ID, first, last, suffix, begin, status, end"
            ).split(', ')
    query = routines.import_query(
            "Sql/nonmember_stati_f.sql").format(
                    helpers.eightdigitdate)
    ret = routines.query2dict_listing(query, keys)
#   for key, value in ret:
#       print(f"{key}: {value}")
    return ret


def get_non_member_stati_cmd(tocsv=True):  # get_non_member_stati.sql
    """
    Returns a header followed by a listing of all
    people with a status OTHER THAN 'm':
    Use for presentation only.
    """
    res = get_non_member_stati()
    n = len(res)
    ret = [
#    13:  34     Angie Calpestri       z4_treasurer
     "People with non member stati",
     "ID     First Last                begin Status end",
     "=================================================",
     ]
    for item in res:
        # each item: ID, first, last, status_key
        ret.append(('{ID:>3}{first:>10} {last:<15}{suffix:<3} '
                    + '{begin} {status} {end}')
                                .format(**item))
    if tocsv:
        csv_file = input(
            "Name of csv file (return if not needed): ")
        if csv_file:
            keys = (
                "ID, first, last, suffix, begin, status, end"
                    ).split(', ')
            with open(csv_file, 'w', newline='') as outf:
                writer = csv.DictWriter(outf, fieldnames=keys)
                writer.writeheader()
                for item in res:
                    writer.writerow(item)
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
    query = routines.import_query("Sql/no_email_f.sql")
    query = query.format(helpers.eightdigitdate)
    res = routines.fetch(query, from_file=False)
    n = len(res)
#   _ = input(res)
    ret = [
     "Member ID, Names and Demographics of {} without email"
     .format(n),]
    ret.append("=" * len(ret[0]))
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
    stati = get_non_member_stati_cmd(tocsv=False)
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
    menu = helpers.get_menu_dict(content.printers.keys())
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
    # choose letter type and assign to holder.which
    response = helpers.get_menu_response(content.ctypes)
    if response == 0:
        ret.append("Quiting per your choice")
        return ret
    w_key = content.ctypes[response-1]  # which_key
    ret = [
        f"Your choice for 'w_key'.. {response:>3}: {w_key}", ]
    holder.which = content.content_types[w_key]
    # which letter has been established & conveyed to the holder
    # now: establish printer to be used and assign templates
#   _ = input(holder.which.keys())
    if {"cc", "bcc"} and set([key for key in holder.which.keys()]):
        holder.cc_sponsors = True
    ret.extend(assign_templates(holder))
    # cc and bcc (incl sponsors) should be done in q_mailing
    # prepare holder for emails
    holder.emails = []
    # collect data..
    for func in holder.which['holder_funcs']:
#       _ = input(f"running holder func {repr(func)}.")
        # assigns holder.working_data (found in routines:
        #   (routines.assign_applicants2welcome,),
        #   (routines.assign_welcome2full_membership,),
        func(holder)
    for dic in holder.working_data.values():
        for func in holder.which['funcs']:  #  vvvvv
#           _ = input(f"Running func {repr(func)}")
            # for billing: members.send_statement(holder, dic)
            # otherwise: members.q_mailing
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



def add_date_cmd():
    ret = ['Adding to applicant dates...']
    # get a personID of the person who's data to modify
    print("Choose from the following...")
    for line in routines.id_by_name():
        print(line)
    personID = int(input(
        "Pick a personID (must be an integer): "))
    # get which date key to modify (provides formatting)
    menu = helpers.get_menu_dict(club.date_keys)
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
    """
    Create a csv file showing all receipts.
    Default file name is "Secret/receipts.csv"
    Presentation is in chronologic order
    unless user chooses presentation by name.
    """
    def s(d):
        names = d['personID'].split()
        name = names[1:]
        name.append(names[0])
        return ''.join(name)

    ret = ['Running receipts_cmd...', ]
    print(ret[0])
    file_name = "Secret/receipts.csv"
    list_of_dicts = []
    fields = ("personID date_received dues dock kayak "
            + "mooring acknowledged ap_fee")
    keys = fields.split()
    fields = ', '.join(keys)
    query = (f"SELECT {fields}  FROM Receipts;")
    ret.append("query is ...")
    ret.append(query)
    for res in routines.fetch(query, from_file=False):
        data = {}
        for n in range(len(keys)):
            data[keys[n]] = res[n]
        names = routines.get_person_fields_by_ID(
                    data['personID'],
                    ('first', 'last', 'suffix', ))
#       _ = input(repr(names))
        data['personID'] = "{first} {last}{suffix}".format(**names)
        list_of_dicts.append(data)
    print(f"Default file name is {file_name}")
    response = input(
        "Enter a different name or leave blank for default... ")
    if response:
        file_name = response
    print("Default is chronologic order.")
    response = input(
            "Would you prefer ordering by name? (y/n) ")
    if response and response[0] in 'yY':
        list_of_dicts.sort(key=s)
    helpers.save_db(list_of_dicts, file_name, data.keys(),
                report=res)


def show_stati_cmd():
    """
    Creates a csv file showing the possible stati.
    """
    outfile = "stati_listed.csv"
    ret = ["Entering show_stati_cmd...", ]
    keys = routines.get_keys_from_schema("Stati")
    query = "SELECT * FROM Stati;"
    res = routines.fetch(query, from_file=False)
    with open(outfile, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=keys)
        writer.writeheader()
        for entry in res:
            writer.writerow(helpers.make_dict(keys, entry))
    ret.append(f"... data written to {outfile}.")
    return ret


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
