#!/usr/bin/env python3

# File: code/commands.py

"""
Most of the code is here.
Driver of the code is main.py
"""

import sqlite3
import sys
import csv
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

def get_command():
    while True:
        choice = input("""   MAIN MENU
Choose one of the following:
  0. Quit (or just return)    1. Show for web site
  2. Show applicants          3. Show names as table
  4. Report                   5. Send letter/email
  6. No email                 7. Get (non member) stati
  8. Update Status            9. Find ID by name
 10. Populate Payables       11. Update demographics
 12. Add Dues                13. Prepare Mailing
 14. Show Applicant Data     15. Add Meeting Date
 16. Not implemented
...... """)
        if ((not choice) or (choice  ==   '0')): sys.exit()
        elif choice ==  '1': return show_cmd
        elif choice ==  '2': return show_applicants
        elif choice ==  '3': return show_names
        elif choice ==  '4': return report_cmd
        elif choice ==  '5': return mailing_cmd
        elif choice ==  '6': return no_email_cmd
        elif choice ==  '7': return get_stati_cmd
        elif choice ==  '8': return update_status_cmd
        elif choice ==  '9': return id_by_name
        elif choice == '10': return populate_payables
        elif choice == '11': return update_people_cmd
        elif choice == '12': return add2dues_cmd
        elif choice == '13': return prepare_mailing_cmd
        elif choice == '14': return get_applicant_data_cmd
        elif choice == '15': return add_date_cmd
        else: print("Not implemented")

# for add_dues:
# UPDATE table SET value = value + 5 WHERE id = 1;

def not_implemented():
    return ["Not implemented", ]

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
    A one time only: add $100 to every one's dues.
    """
    query = """
        UPDATE Dues SET dues_owed = dues_owed + 100;
        """
    con = sqlite3.connect(club.DB)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return ['executed:', query]


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
#               db=club.DB,
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
    WHERE {}
    ;
    """
    print("Looking for people:")
    print("Narrow the search, use * to eliminate a blank...")
    first = input("First name (partial or blank): ")
    last = input("Last name (partial or blank): ")
    if first and last:
        query = query.format("first LIKE ? AND last LIKE ? ")
    elif first:
        query = query.format("first LIKE ?")
    elif last:
        query = query.format("last LIKE ? ") 
    params = [name+'%' for name in (first, last,) if name]
#   print(params)
    ret = routines.fetch(
                query,
#               db=club.DB,
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
    """
    headers = ('No meetings', 'Attended one meeting',    # 0, 1
        'Attended two meetings',                         # 2
        'Attended three (or more) meetings',             # 3
        'Approved (membership pending payment of dues)', # 4
        )
    # not sure the next two are being used!!
    date_keys = club.date_keys
    sponsor_keys = club.sponsor_keys
    
    query_file = 'Sql/applicants2.sql'
    res = routines.fetch(query_file)
    # convert our returned sequences into...
    dics = []        #  a sequence of dicts:
    for sequence in res:
        key_value_pairs = zip(club.appl_keys, sequence)
        mapping = {}
        for key, value in key_value_pairs:
            mapping[key] = value
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
    res = routines.fetch('Sql/names.sql')
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
        print('\n'.join(id_by_name()))
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

def assign_printer(holder):
    """ assign printer to use..."""
    ret = []
#   print("About to call content.assign_printer")
#   content.assign_printer(holder)  # as yet unresolved bug!!
    menu = routines.get_menu_dict(content.printers.keys())
    print("Printer to use...")
    for key, lpr in menu.items():
        print(f"{key}: {lpr}")
    index = int(input("Which printer to use? "))
    holder.printer = menu[index]
    ret.append(
        f"          for 'printer'.. {index:>3}: {holder.printer}")
    return ret


def assign_templates(holder):
    """ assign letter template..."""
    ret = []
    ret.append("letter_template follows...")
    holder.letter_template = content.prepare_letter_template(
            content.content_types[holder.which],
            content.printers[holder.printer])
    ret.append(holder.letter_template)
    ret.append("...end of letter_template for '{holder.which}'.")
    ret.append("emal_template follows...")
    holder.email_template = content.prepare_email_template(
            content.content_types[holder.which])
    ret.append(holder.email_template)
    ret.append("...end of email_template for '{holder.which}'.")
    return ret

def assign_owing(holder):
    """
    Assigns holder.owed_by_id dict:
    Retrieve personID for each person who owes
    putting their relevant data into a dict keyed by ID.
    """
    ret = []
    byID = dict()
    # dues owing:
    for tup in (routines.fetch("Sql/dues.sql")):
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'dues_owed': tup[4],
                        }
    # dock privileges owing:
    for tup in routines.fetch("Sql/dock.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['dock'] = tup[1]
    # kayak storage owing:
    for tup in routines.fetch("Sql/kayak.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['kayak'] = tup[1]
    # mooring fee owing:
    for tup in routines.fetch("Sql/mooring.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['mooring'] = tup[1]
    # return what's been collected:
    holder.owed_by_id = byID
    return ret


def prepare_invoice(holder, personID):
    """
    holder.owed_by_id has already been assigned
    returns an iterable of strings that when '\n'.joined
    provides an invoice statement.
    """
    total = 0
    invoice = [f"Statement as of {helpers.today}:",]]
    for key, value in holder.owed_by_id[personID].items():
        invoice.append(f"    {key:<10} {value}")
        total += value
    invoice.append(f"        Total: ${total}")
    return invoice


def prepare_mailing(holder):
    """
    Populates attributes 'holder'.
    Early stages of development: assume doing dues & fees.
    """
    ret = []
    ret.extend(assign_printer(holder))
    ret.extend(assign_templates(holder))
#   for key, value in byID.items():
#       ret.append(f"{key}: {repr(value)}")
    return ret


def prepare_mailing_cmd():
    """
    Sets up & then calls prepare_mailing
    """
    # Determine content type desired...
    holder = club.Holder()
    ret = []
    response = routines.get_menu_response(content.ctypes)
    if response == 0:
        ret.append("Quiting per your choice")
        return
    holder.which = content.ctypes[response-1]
    ret = [f"Your choice for 'which'.. {response:>3}: {holder.which}", ]
    # which letter has been established & conveyed to the holder
    # hand control over to prepare_mailing...
    ret.extend(prepare_mailing(holder))
#   for key, value in content.content_types[holder.which].items():
#       ret.append(f"%% {key:>13} %%: {value}")
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
        ret = id_by_name()
        for line in ret:
            print(line)
    appID = input("Enter ID: ")
    if not appID:
        print("Lack of entry ==> termination!")
        sys.exit()
    return show_applicant_data(appID)


def mailing_cmd():
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
    for line in id_by_name():
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
    query = """/* Sql/insert_date.sql */
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


if __name__ == "__main__":
#   with open("4Angie.csv", 'w', newline='') as csvfile:
#       fieldnames = ('last', 'first')
#           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#           writer.writeheader()
#           for entry in for_angie():
#               writer.writerow(
#                   {'last': entry[0], 'first': entry[1]})
#   print(for_angie())
#   try_applicants()
    print(get_emailing_dict(101))
