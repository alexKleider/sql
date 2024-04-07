#!/usr/bin/env python3

# File: code/routines.py

"""
Contains some 'helper' code to support SQL(ite3)
relational data base management.

Contains the "funcs" typified by std_mailing_funcs:
    it's here than "extra[n]" field might be added for such things
    as billing statement or the like.
"""

import os
import csv
import shutil
import sqlite3
try: from code import club
except ImportError: import club
try: from code import helpers
except ImportError: import helpers

db_file_name = club.db_file_name

def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("clubcursor")
    """
    try:
        db = sqlite3.connect(path)
        clubcursor = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:", path)
        db, clubcursor = None, None
        raise
    return db, clubcursor


def closeDB(database, cursor):
    try:
       cursor.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise
 

def assure_only1response(listing):
    """
    Does nothing if len(listing)==1!
    Otherwise...
    <listing> is a query response
    Stops execution if it contains more than one row.
    Use when exactly one response is expected.
    """
    if len(listing) != 1:
        print(f"listing contains {len(listing)} item(s)...")
        for item in listing:
            print(item)
        print("Time to quit!")
        sys.exit()


def add2report(report, line, also_print=False):
    """
    This should be incorporated into code.helpers
    Supports many routines which have a named 'report' param.
    """
    if isinstance(report, list):
        if isinstance(line, str):
            report.append(line)
            if also_print: print(line)
        elif isinstance(line, list):
            report.extend(line)
            if also_print:
                for l in line: print(l)


def fetch(sql_source, db=db_file_name, params=None, data=None,
                    from_file=True, commit=False,
                    verbose=False):
    """
    <sql_source> must be a string: either the name of a file
    containing a valid sqlite3 query or (if <from_file> is set
    to False) the query itself. The query is executed on the <db>.
    Only one (if any) of the following should be provided:
        <params> must be an iterable of length to match number
            of qmark placeholders in the query. Remember to use
            the '%' character as a suffix (or prefix or both.)
        <data> must be a dict with all keys necessary to match
            all place holders in the query. Remember place holder
            names are prefaced by a colon in the query.
            eg: (:key1, :key2).
    Be aware that the query might return an empty list.
    """
    if from_file:
        with open(sql_source, 'r') as source:
            query = source.read()
#       _ = input(f"### Query begins next line\n{query}")
    else: query = sql_source
#   print(query)
    db, cur = initDB(db)
    if data:
        cur.executemany(query, data)
    elif params:
#       _ = input(f"params set to '{params}'")
        cur.execute(query, params)
    else:
        cur.execute(query)
#   _ = input(
#       f"get_query_result returning the following:\n {ret}")
    ret = cur.fetchall()
    if commit:
        db.commit()
        if verbose:
            _ = input("Committed!")
    closeDB(db, cur)
    if verbose:
        print(f"routines.fetch returning {ret}")
    return ret


def import_query(sql_file_name):
    """
    Returns the content of <sql_file_name>
    (assumed to be a text file.)
    Typically used for queries that require formatting.
    """
    with open(sql_file_name, 'r') as inf:
        return(inf.read())

def fetch_d_query(sql_file_name, data, commit=False):
    """
    Assumes <sql_file_name> is a file containting an SQL query
    with place holders keyed by key/value pairs available
    in <data>, a dict.
    """
    query = import_query(sql_file_name)
    query = query.format(**data)
#   _ = input(f"fetch_d_query param is\n{query}")
    return fetch(query, from_file=False, commit=commit)


def keys_from_schema(table, brackets=(0,0)):
    """
    query comes from: https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    <brackets> provides ability to ignore first brackets[0]
    and last brackets[1] primary keys such as 'personID' (in
    which case it can be set to (1,0).
    Tested in tests/test_routines.py
    """
    query =  f"pragma table_info({table})"
    res = fetch(query, from_file=False)
    begin = brackets[0]
    end = len(res) - brackets[1]
    return  [item[1] for item in res[begin:end]]
    # item[1] is the column/key.


def keys_from_query(query):
    """
    Returns a listing of keys requested in the query
    """
    nselect = query.find("SELECT")
    nfrom = query.find("FROM")
    keystring = query[nselect+6:nfrom]
    nowhitespace = ''
    for ch in keystring:
        if ch.split():
            nowhitespace = nowhitespace + ch
    keys = nowhitespace.split(",")
    splitkeys = [key.split('.') for key in keys]
    return [key[-1] for key in splitkeys]


def query2dict_listing(query, keys,
                       from_file=False):
    """
    Returns query result as a (could be empty!) list of dicts
    (which can be dumped into a json file.)
    Fails if len(keys)!=length of tupples returned by the query.
    <keys> parameter typically supplied by keys_from_schema()
    or keys_from_query.
    """
    ret = []
    res = fetch(query, from_file=from_file)
    for entry in res:
        d = dict(zip(keys, entry))
        ret.append(d)
    return ret

def query2dicts(query, from_file=False):
    """
    Returns a (possibly empty) list of dicts.
    """
    if from_file:
        query = import_query(query)
    return query2dict_listing(query,
            keys_from_query(query))


def display(instance, exclude=None):
    """
    A utility best put into helpers.
    Used to discover attributes of an instance.
    They are returned as a list (exclusive of dunder values.)
    """
    ret = ["Displaying..", ]
    for item in instance.__dir__():
        if item.startswith('__'):
            continue
        if item in exclude:
            continue
        insertion = eval(f'instance.{item}')
        if isinstance(insertion, dict):
            for key, value in insertion.items():
                ret.append(f"{key}: {value}")
            else:
                ret.append(f"{item}: {insertion}")
        ret.append(".. end of display.")
        return ret


def execute(cursor, connection, command, params=None):
    try:
        if params:
            cursor.execute(command, params)
        else:
            cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
#   _ = input(command)
#   if commit:
#       connection.commit()


def connect_and_get_data(command, db=db_file_name):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(command)
    return cur.fetchall()


def connect_and_set_data(command, db=db_file_name):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(command)
    con.commit()


def get_ids_by_name(first, last, db=db_file_name):
    """
    Returns People.personID (could be more than one!)
    for anyone with <first> <last> name.
    Returns a (possible empty) tuple.
    Unlikely it'll ever be more than a tuple with one value
    """

    query = f"""SELECT personID, first, last, suffix from People
            WHERE People.first = "{first}"
            AND People.last = "{last}" """
#   _ = input(query)
    con = sqlite3.connect(db)
    cur = con.cursor()
    execute(cur, con, query)
    res = cur.fetchall()
    if not res:
        _ = input("No key for {} {}".format(first, last))
    return res


def get_people_fields_by_ID(db_file_name=db_file_name,
                                    fields=None):
    """
    ## What is this for???
    Select values of the <fields> columns from the People table.
    Default (<fields> not specified) is to select all fields.
    """
    ret = {}
    query = """SELECT {} FROM People;"""
    if fields:
        fields = ["personID", ] + [field for field in fields]
        var = ', '.join(fields)
    else: var = '*'
    query = query.format(var)
#   _ = input(query)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, query.format(var))
    res = cur.fetchall()
#   _ = input(res)
    for entry in res:
        ret[entry[0]] = entry[1:]
    return ret


def get_person_fields_by_ID(personID, fields=None):
    """
    Select values of the <fields> columns from the People table
    for the personID specified.
    Returns a dict keyed by names of fields
    `_if_ <fields> is provided (as an iterable,)
     _otherwise_ returns a tuple of all fields.
    """
#   _ = input("Entering code/routines.get_person_fields_by_ID")
    query = """SELECT {{}} FROM People
    WHERE personID = {};""".format(personID)
    if fields:
        fields = [field for field in fields]
        var = ', '.join(fields)
    else: var = '*'
    query = query.format(var)
#   _ = input(query)
    res = fetch(query, from_file=False)[0]  # Note the '[0]'
    if fields:
        dic = {}
        z = zip(fields, range(len(fields)))
        for field, n in z:
            dic[field] = res[n]
#       for key, value in dic.items():
#           print(f"'{key}': '{value}'")
#       _ = input("^dict version of query^")
        return dic
    else:
#       _ = input(res)
        return res


def get_people_fields_by_ID(db_file_name=db_file_name,
                                    fields=None):
    """
    Select values of the <fields> columns from the People table.
    Default (<fields> not specified) is to select all fields.
    """
    ret = {}
    query = """SELECT {} FROM People;"""
    if fields:
        fields = ["personID", ] + [field for field in fields]
        var = ', '.join(fields)
    else: var = '*'
    query = query.format(var)
#   _ = input(query)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, query.format(var))
    res = cur.fetchall()
#   _ = input(res)
    for entry in res:
        ret[entry[0]] = entry[1:]
    return ret


def get_name(personID):
    if not personID:
        return ""
    name_query = """SELECT first, last, suffix
            FROM People
            WHERE personID = ?;"""
    res = fetch(name_query, 'Secret/club.db',
            from_file=False, params=[personID, ])[0]
    suffix = res[2]
    if suffix:
        suffix = f" {suffix}"
    return "{0:} {1:}".format(*res) + suffix


def id_by_name():
    """
    Returns a listing of strings: '{Id} {first} {last} {suffix}'
    from the 'People' table (together with IDs.)
    Prompts for first letter(s) of first &/or last name(s).
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
    else:  # no entry provided
        return
    params = [name+'%' for name in (first, last,) if name]
#   print(params)
    ret = fetch(
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


def get_commands(sql_file):
    """
    Assumes <in_file> contains valid SQL commands.
    i.e. could be read by sqlite> .read <in_file>
    Yeilds the commands one at a time.
    Usage:
        con = sqlite3.connect("sql.db")
        cur = con.cursor()
        for command in get_commands(sql_commands_file):
            cur.execute(command)
    """
    with open(sql_file, 'r') as in_stream:
        command = []
        for line in in_stream:
            parts = line.split('--')
            line = parts[0]
            line = line.strip()
            if ((not line)
            or ((len(line) == 1)
                and (not line[0] in ';)'))):
                continue
            command.append(line)
            if line.endswith(';'):
                yield ' '.join(command)
                command = []


people_query = """/* Sql/get_by_ID_f.sql */
        SELECT * FROM People WHERE personID = {};
        """
like_query = """
        SELECT * FROM People WHERE {};
        """

def get_rec_by_ID(ID):
    """
    Returns a record corresponding to personID if record
    exists, otherwise returns None
    (Client is pick_People_record)
    """
    res = fetch(people_query.format(ID), from_file=False)
#   _ = input(res)
    if not res:
        return
    ret = helpers.make_dict(
            keys_from_schema("People"), res[0])
#                               from_file=False)
    if not ret:
        return
    else:
        return ret


def pick_People_record(header_prompt=None, report=None):
    """
    Returns either a dict representing a person in the People
    table...  or None.
    Prompts for name clues (which can be ignored)
    #?Makes id_by_name() redundant??
    """
    if isinstance(report, list):
        report.append(
                "... entering routines.pick_People_record()")
    keys = keys_from_schema("People")
    if header_prompt: print(header_prompt)
    while True:
        print(
          "Narrow the search (blanks if ID known)...")
        first = input("First name (partial or blank): ")
        last = input("Last name (partial or blank): ")
        if first and last:
            query2use = like_query.format(
                f"first LIKE '{first}%' AND last LIKE '{last}%'")
        elif first:
            query2use = like_query.format(
                    f"first LIKE '{first}%'")
        elif last:
            query2use = like_query.format(f"last LIKE '{last}%'") 
        else:  # no entry provided
            query2use = listing = None
        if query2use:
            res = fetch(
                    query2use,
    #               db=club.DB,
                    from_file=False,
                    )
            listing = [helpers.make_dict(keys, entry)
                                    for entry in res]
        if listing:
            choices = [d['personID'] for d in listing]
            print("Choose an ID from one of the following:")
            for d in listing:
                print("{personID:3>} {first} {last} {suffix}"
                                            .format(**d))
        ID = input("Enter a personID (0 to exit):  ")
        try:
            ID = int(ID)
        except ValueError:
            report.append(
                "..non integer entered; restarting..")
            print(report[-1])
            continue
        else:
            if ID == 0:
                if isinstance(report, list):
                    report.append(
                    "... '0' entry ==> exit pick_People_record.")
                return
        if listing and ID in choices:
            for d in listing:
                if d['personID'] == ID:
#                   print(f"returning: {d}")
                    if isinstance(report, list):
                        report.append(
                            f"pick_People_record => \n{repr(d)}")
                    return d
        else:
            rec = get_rec_by_ID(ID)
            if not rec:
                if isinstance(report, list):
                    report.append(
                        "... no such ID: starting over ..")
                continue
            else:
                if isinstance(report, list):
                    report.append(
                        "... pick_People_record => a dict.")
                return rec


def dict_from_list(listing, fields):
    """
    <listing> is an iterable as might be an element in what's
    returned by an SQL query.
    <fields> is an array of (word, integer, ) tuples that
    determines which entry in the listing is keyed by what
    <word> in the resulting dict.
    """
    ret = {}
    for word, i in fields:
        ret[word] = listing[i]
    return ret


def compound_dict_from_query(listings, fields,
                        key_name_and_index):
    """
    The first two params are used to create 
    """
    ret = {}
    for listing in listings:
        d_from_list = dict_from_list(listing, fields)
        ret[key_name_and_index[0]] = listing[
                            key_name_and_index[1]]

def ret_statement(personID, incl0=True):
    """
    Returns a (possibly empty) dict.
    Key/value pairs are account (dues, dock, etc)
    and amount owing (including where value is 0.)
    """
    source_files = {
            # the following files all check for membership.
            # hence the 'f' for formatted by
            # helpers.eightdigitdate
            # the "0" indicates that zero balances are included
            'dues': "Sql/dues0_f_byID.sql",
            'dock': "Sql/dock0_f_byID.sql",
            'kayak': "Sql/kayak0_f_byID.sql",
            'mooring': "Sql/mooring0_f_byID.sql",
            }
    ret = {"total": 0, }
    total = 0
    entry = False
    for key in source_files.keys():
        query = import_query(source_files[key])
        query = query.format(helpers.eightdigitdate,
                             helpers.eightdigitdate)
        query = query.format(personID)
        res = fetch(query, from_file=False)
#       if personID == 171:   # 2Delete 2lines
#           _ = input(res)
        print(query)
        print(repr(res))
        if res:
            amnt = res[0][0]
            if len(res)>1:
                assert(False), 'Error in routines.ret_statement.'
            ret[key] = amnt
            total += amnt
            entry = True
    if entry: ret['total'] = total
    return ret  # a dict possibly with only one (total) entry.

def get_data4statement(personID):
    """
    Returns a dict keyed by the following:
    personID, first, last, suffix,
    address, town, state, postal_code, country,
    email, dues_owed
    and if applicable:
    dock, kayak, mooring.
    If no result from the query: returns an empty dict.
    """
    data = {'personID': personID,
            }
    res = fetch("Sql/demographics_by_ID.sql",
                    params=(personID, ) )[0]
    data['first'] = res[0]
    data['last'] = res[1]
    data['suffix'] = res[2]
    data['address'] = res[3]
    data['town'] = res[4]
    data['state'] = res[5]
    data['postal_code'] = res[6]
    data['country'] = res[7]
    data['email'] = res[8]
    data2add = ret_statement(personID)
    for key in data2add.keys():
        data[key] = data2add[key]
    return data

def get_statement(data, include_header=True):
    """
    <data> is a dict returned by get_data4statement.
    Returns a multiline string: a statement of what's owed
    as reflected in the .
        "Currently owing" (dues, dock, kayak, mooring),
        and "total" keys of <data>.
    """
    if include_header: owing = ["Currently owing:", ]
    else: owing = []
    keys = set(data.keys())
#   for key, value in data.items():   # 2delete 3lines
#       print(f"{key}: {value}")
#   _ = input('Check the above for a "dues" key')
    owing.append(    f"  Dues owing..... {data['dues']:>3}")
    if "dock" in keys:
        owing.append(f"  Dock usage..... {data['dock']:>3}")
    if "kayak" in keys:
        owing.append(f"  Kayak storage.. {data['kayak']:>3}")
    if "mooring" in keys:
        owing.append(f"  Mooring fee.... {data['mooring']:>3}")
    owing.append(f"Total... ${data['total']}")
    return '\n'.join(owing)

def get_owing(holder):
    """
    Assigns holder.working_data dict:
    Retrieve personID for each person who owes
    putting their relevant data into holder.working_data:
    a dict keyed by ID.
    """
    byID = dict()  # to be assigned to holder.working_data
    res = fetch('Sql/dues0')
    pass


def assign_mannually(holder):
    """
    Assigns holder.working_data to an empty dict
    and then prompts user to add entries.
    Used to assign recipients of mailing.
    """
    holder.working_data = {}
    while True:
        rec = pick_People_record(
                header_prompt="Selecting a record...")
        if rec:
            holder.working_data[rec['personID']] = rec
        else:
            response = input("Done with entries? (y/n) ")
            if response and response[0] in 'yY':
                break

def add_sponsors2holder_data(holder):
    """
    Adds sponsorIDs (if they exist) to all the records
    in holder.working_data (which is People table data
    keyed by personID.
    Note: adds sponsorIDs, not names
    """
    query = "SELECT * from Applicants where personID = {};"
    ap_keys = keys_from_schema("Applicants")
    for key in holder.working_data.keys():
        res = fetch(query.format(key), from_file=False)
        if res:
            ap_dict = helpers.make_dict(ap_keys, res[0])
            for sponsor in ("sponsor1ID", "sponsor2ID"):
                holder.working_data[key][sponsor] = (
                        ap_dict[sponsor])
        else:
            for sponsor in ("sponsor1ID", "sponsor2ID"):
                holder.working_data[key][sponsor] = ''


def assign_owing(holder):
    """
    Assigns holder.working_data dict:
    Retrieve personID for each person who owes
    putting their relevant data into a dict keyed by ID.
    """
    byID = dict()
    query = import_query("Sql/members_f.sql"
                        ).format(helpers.eightdigitdate,
                                 helpers.eightdigitdate)
    for tup in fetch(query,
            from_file=False):
        personID = tup[0]
        data  = {'first': tup[1],
                 'last': tup[2],
                 'suffix': tup[3],
                 'email': tup[4],
                 'address': tup[5],
                 'town': tup[6],
                 'state': tup[7],
                 'postal_code': tup[8],
                 'country': tup[9],
                }
        data2add = ret_statement(personID)
        if data2add:
            for key in data2add.keys():
                data[key] = data2add[key]
            byID[personID] = data
    holder.working_data = byID


def assign_inductees4payment(holder):
    """
    Assigns holder.working_data dict keyed by ID pertaining
    to those recently inducted and yet to be notified.
    REFACTOR to use add_sponsor_cc2data
    """
    byID = dict()
    res = fetch('Sql/inducted.sql')
    keys = ("personID last first suffix phone address town state"
    + " postal_code email sponsor1ID sponsor2ID begin end")
    ## sponsor1 and sponsor2 are IDs!!
    keys = keys.split()
    # Now get the sponsors...
    query = """SELECT last, first, suffix, email FROM People
            WHERE personID = {};"""  # returns a one entry list
    sponsor_keys = "last first suffix email"
    for line in res:  # what's collected by Sql/inducted.sql
        data = helpers.make_dict(keys[:],
                line[:])
        data['cc'] = []
        data['sponsor1'] = helpers.make_dict(
                sponsor_keys.split(),
                fetch(query.format(data['sponsor1ID']),
                from_file=False)[0])  # '[0]' is to get first
                                    # of a one entry list
        if data['sponsor1']['email']:
            data['cc'].append(data['sponsor1']['email'])
        data['sponsor2'] = helpers.make_dict(sponsor_keys.split(),
                fetch(query.format(data['sponsor2ID']),
                from_file=False)[0])
        if data['sponsor2']['email']:
            data['cc'].append(data['sponsor2']['email'])
        data['cc'] = ','.join((data['cc']))
        byID[line[0]] = data
    holder.working_data = byID

def getIDs_by_status(statusID):
    query = import_query(
        "Sql/ids_by_status_f.sql").format(
            statusID, helpers.eightdigitdate)
    res = fetch(query, from_file=False)
    return [entry[0] for entry in res]


def add_sponsorIDs(data):
    """
    <data> is a dict assumed to have fields sponsor1 & sponsor2.
    Returns data with fields sponsor1ID and sponsor2ID.
    Modifies data (passed by reference since it's mutable.
    """
    for spName, spID in (('sponsor1', 'sponsor1ID'),
                        ('sponsor2', 'sponsor2ID'),):
        while True:
            res = pick_People_record(header_prompt=
                            f'Listed sponsor is: {data[spName]}')
            to_show = (
                    "{personID} {first} {last} {suffix}"
                        .format(**res))
            yn = input(f"Accept {to_show}? y/n: ")
            if yn and yn[0] in yn:
                data[spID] = res['personID']
                break

def add_sponsors2data(data):
    """
    <data> is a record/dict
    If it has <sponsor[1,2]ID key then
    We add <sponsor[1,2]> keys the value of each containing
    a record of first, last, suffix, email of each sponsor.
    Note: the sponsor may not have email.
    """
    applicantID = data["personID"]
    sponsorIDs = fetch("""
        SELECT sponsor1ID, sponsor2ID FROM Applicants
        WHERE personID = ?; """,
        params=(applicantID,), from_file=False)
    sponsors = []
    sponsor_keys = 'first, last, suffix, email'.split(', ')
    for sponsorID in sponsorIDs[0]:
#       _ = input(f"sponsorID: {sponsorID}")
        sponsor = fetch("""
        SELECT first, last, suffix, email FROM People
        WHERE personID = ? AND notified = '';""",
        params=(sponsorID,), from_file=False)
        sponsors.append(dict_from_list(sponsor, sponsor_keys))
    data['sponsor1ID'] = sponsorIDs[0][0]
    data['sponsor2ID'] = sponsorIDs[0][1]
    data['sponsor1'] = sponsors[0]
    data['sponsor2'] = sponsors[1]
    return data


def add_sponsor_data(data):
    """
    <data> is a record, its first field is personID.
    Added are the following fields:
        sponsor1ID, sponsor2ID, sponsor1, sponsor2
    sponsor[1/2] are records of first, last, suffix, email
    the email field possibly being empty.
    """
    sponsorIDs = fetch("""
        SELECT sponsor1ID, sponsor2ID FROM Applicants
        WHERE personID = ?; """,
        params=(data['personID'],), from_file=False)
    sponsors = []
    sponsor_keys = "first, last, suffix, email".split(', ')
    data['sponsor1ID'] = sponsorIDs[0][0]
    data['sponsor2ID'] = sponsorIDs[0][1]
    res = fetch("""
            SELECT first, last, suffix, email FROM People
            WHERE personID = ?""",
            params=(sponsorIDs[0][0],), from_file=False)
#   print(f"{res}")
#   _ = input(f"{sponsor_keys}")
    data['sponsor1'] = helpers.make_dict(sponsor_keys, res[0])
    res = fetch("""
            SELECT first, last, suffix, email FROM People
            WHERE personID = ?""",
            params=(sponsorIDs[0][1],), from_file=False)
    data['sponsor2'] = helpers.make_dict(sponsor_keys, res[0])


def get_sponsors(applicantID):
    sponsorIDs = fetch("""
        SELECT sponsor1, sponsor2 FROM Applicants
        WHERE personID = ?; """,
        params=(applicantID,), from_file=False)
    sponsors = []
    for sponsorID in sponsorIDs[0]:
#       _ = input(f"sponsorID: {sponsorID}")
        sponsors.append(fetch("""
        SELECT first, last, suffix, email FROM People
        WHERE personID = ?""",
        params=(sponsorID,), from_file=False))
    return sponsors


def add_sponsor_cc2data(data):
    """
    <data> must be a dict with sponsor1ID and sponsor2ID keys
    who's values are personIDs. 
    A data['cc'] entry is created as a string with sponsor
    emails separated by commas. The string could be empty
    if sponsors don't have email.
    """
    query = """SELECT last, first, suffix, email FROM People
            WHERE personID = {};"""  # returns a one entry list
    sponsor_keys = "last first suffix email"
    data['cc'] = []
    for sponsor in ('sponsor1ID', 'sponsor2ID'):
        sponsor_dict = helpers.make_dict(sponsor_keys.split(),
            fetch(query.format(data[sponsor]),
                from_file=False)[0])  # '[0]' is to get first
                                    # of a one entry list
        if sponsor == 'sponsor1ID':
            data['sponsor1'] = sponsor_dict
        if sponsor == 'sponsor2ID':
            data['sponsor2'] = sponsor_dict
        if sponsor_dict['email']:
            data['cc'].append(sponsor_dict['email'])
    data['cc'] = ','.join(data['cc'])


def assign_applicant_fee_pending(holder):
#   assignees = getIds_by_status(1)
    query = import_query("Sql/applicants_of_status_ff.sql")
    query = query.format(1, helpers.eightdigitdate)
    res = fetch(query, from_file=False)
    keys = ("personID, last, first, suffix, phone, " +
        "address, town, state, postal_code, email, " +
        "sponsor1ID, sponsor2ID, app_rcvd, fee_rcvd, " +
        "meeting1, meeting2, meeting3, approved, " +
        "dues_paid, notified, begin, end").split(', ')
    listing = []
    byID = {}
    for entry in res:
        mapping = dict(zip(keys, entry))
        listing.append(mapping)
        byID[entry[0]] = mapping
    holder.working_data = byID

def assign_just_me(holder):
    query = """SELECT * FROM People WHERE
            first = "Alex" AND last = "Kleider";"""
    res = fetch(query, from_file=False)
    keys = keys_from_schema("People")
    listing = []
    byID = {}
    for entry in res:
        mapping = dict(zip(keys, entry))
        listing.append(mapping)
        byID[entry[0]] = mapping
    holder.working_data = byID

def assign_applicants2welcome(holder):
#   assignees = getIds_by_status(2)
    query = import_query("Sql/applicants_of_status_ff.sql")
    query = query.format(2, helpers.eightdigitdate)
    res = fetch(query, from_file=False)
    keys = ("personID, last, first, suffix, phone, " +
        "address, town, state, postal_code, email, " +
        "sponsor1ID, sponsor2ID, app_rcvd, fee_rcvd, " +
        "meeting1, meeting2, meeting3, approved, " +
        "dues_paid, notified, begin, end").split(', ')
    listing = []
    byID = {}
    for entry in res:
        mapping = dict(zip(keys, entry))
        listing.append(mapping)
        byID[entry[0]] = mapping
    holder.working_data = byID
    print("Now need to update applicant's status from 2 > 3.")


def assign_welcome2full_membership(holder):
    ret = ['<welcome to full_membership mailing>',
            ]
    print("Create list of people to welcome as new member(s):")
    candidates_byID = {}
    while True:
        candidate = pick_People_record("Pick a person...")
        if not candidate:
            break
        else:
            candidates_byID[candidate['personID']] = candidate
    if not candidates_byID:  # nothing to do
        ret.append("No candidate(s) specified. Nothing to do.")
        return ret
    for ID in candidates_byID.keys():
        add_sponsor_data(candidates_byID[ID])
    holder.working_data = candidates_byID
    add_sponsors2holder_data(holder)
    return ret


def db2csv(report=None):
    """
    Backs up the data base (Secret/club.db) by creating a csv file
    for each table, putting them all into a separate directory,
    and then creating a zip file to be backed up on Google Drive.
    """
    if not report:
        report = []
    tempdir = "TempZIP_Dir"
    zip_name = f"{helpers.eightdigitdate4filename}_db_bu_as_CSVs"
    tables = fetch(
            """SELECT name FROM sqlite_master
               WHERE type='table';""", from_file=False)
    tables = [table[0] for table in tables]
    os.mkdir(tempdir)
    for table in tables:
        file_name = tempdir +'/' + f"{table}.csv"
        keys = keys_from_schema(table)
        with open(file_name, 'w', newline='') as stream:
            csv_writer = csv.writer(stream)
            csv_writer.writerow(keys_from_schema(table))
            res = fetch(f"SELECT * FROM {table};",
                    from_file=False)
            for row in res:
                csv_writer.writerow(row)
    archived = shutil.make_archive(zip_name, 'zip', tempdir)
    report.append("created: " + repr(archived))
    print(report[-1])
    shutil. rmtree(tempdir)
    return report

if __name__ == "__main__":
    db2csv()


def exercise_get_person_fields_by_ID(id_n):
    print(get_person_fields_by_ID(id_n,
            fields = ('first', 'last', 'suffix')))

def exercise_getIDs_by_status(statusID):
    print(getIDs_by_status(statusID))

def exercise_assign_applicants2welcome():
    holder = dict()
    for entry in assign_applicants2welcome(holder):
        print(entry)

def exercise_add_sponsor_cc2data():
    data = {'sponsor1': 4,
            'sponsor2': 89,
            }
    add_sponsor_cc2data(data)
    for key, value in data.items():
        print(f"{key}: {value}")

def exercise_pick_People_record():
    while True:
        res = pick_People_record(
            header_prompt="Exercising pick_People_record")
        print(f"{res}")


def exercise_keys_from_schema():
    for schema in ("People", "Person_Status", "Stati",
            "Attrition", "Applicants", "Receipts", "Dues",
            "Moorings", "Dock_Privileges", "Kayak_Slots" ):
        print(f"{schema}: " +
            f"{repr(keys_from_schema(schema))}")

def exercise_add_sponsorIDs():
    data = dict(sponsor1= "Alex Kleider some date",
                sponsor2= "June Kleider some other date",
                )
    add_sponsorIDs(data)
    print(f"new data: {repr(data)}")

def test_id_by_name():
    while True:
        # exit using ^D
        _ = input(repr(id_by_name()))

if __name__ == '__main__':
#   print(get_sponsors(110))
#   exercise_get_person_fields_by_ID(146)
#   print("\nWhat follows are three statements:....")
#   print(get_statement(get_data4statement(197)))
#   print(get_statement(get_data4statement(42)))
#   print(get_statement(get_data4statement(157)))
#   exercise_getIDs_by_status(200)
#   exercise_assign_applicants2welcome()
#   exercise_add_sponsor_cc2data()
#   exercise_pick_People_record()
#   exercise_keys_from_schema()
#   exercise_add_sponsorIDs()
    test_id_by_name()
