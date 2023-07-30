#!/usr/bin/env python3

# File: code/routines.py

"""
Contains some 'helper' code to support SQL(ite3)
relational data base management.
"""

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
 

def fetch(sql_source, db=db_file_name,
                    params=None, data=None,
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
    return ret


def import_query(sql_file_name):
    """
    Returns the content of <sql_file_name>
    (assumed to be a text file.)
    """
    with open(sql_file_name, 'r') as inf:
        return(inf.read())

def fetch_d_query(sql_file_name, data, commit=False):
    """
    Assumes <sql_file_name> is a file containting an SQL query
    with place holders keyed by key/value pairs s available
    in <data>, a dict.
    """
    query = import_query(sql_file_name)
    query = query.format(**data)
#   _ = input(f"fetch_d_query param is\n{query}")
    return fetch(query, from_file=False, commit=commit)


def get_keys_from_schema(table, nkeys2ignore=0):
    """
    query comes from: https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    <nkeys2ignore> provides ability to ignore any primary keys
    such as 'personID' (in which case it can be set to 1.
    """
    query =  f"pragma table_info({table})"
    res = fetch(query, from_file=False)
    return  [item[1] for item in res[nkeys2ignore:]]
    # item[1] is the column/key.

def query2dict_listing(query, keys,
                       from_file=False):
    """
    Assumes len(keys)==length of each tupple returned by the
    query.
    """
    ret = []
    res = fetch(query, from_file=from_file)
    for entry in res:
        d = dict(zip(keys, entry))
        ret.append(d)
    return ret


def display(instance, exclude=None):
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
    Returns a dict keyed by names of fields _if_ <fields> is
    provided, _otherwise_ returns a tuple of all fields.
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

def get_sponsors(applicantID):
#   print(f" applicantID: {applicantID} {type(applicantID)}")
    sponsorIDs = fetch("""
        SELECT sponsor1, sponsor2 FROM oldApplicants
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
    ret = {}
    total = 0
    entry = False
    for key in source_files.keys():
        query = import_query(source_files[key]
                            ).format(helpers.eightdigitdate)
        res = fetch(query.format(personID), from_file=False)
#       if personID == 179:
#           _ = input(res)
        if res:
            amnt = res[0][0]
            if len(res)>1:
                assert(False)
            ret[key] = amnt
            total += amnt
            entry = True
    if entry: ret['total'] = total
    return ret  # a possibly empty dict

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


def assign_owing(holder):
    """
    Assigns holder.working_data dict:
    Retrieve personID for each person who owes
    putting their relevant data into a dict keyed by ID.
    """
    byID = dict()
    query = import_query("Sql/members_f.sql"
                        ).format(helpers.eightdigitdate)
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
    + " postal_code email sponsor1 sponsor2 begin end")
    keys = keys.split()
    query = """SELECT last, first, suffix, email FROM People
            WHERE personID = {};"""  # returns a one entry list
    sponsor_keys = "last first suffix email"
    for line in res:
        data = make_dict(keys[1:],
                line[1:])
        data['cc'] = []
        data['sponsor1'] = make_dict(sponsor_keys.split(),
                fetch(query.format(data['sponsor1']),
                from_file=False)[0])  # '[0]' is to get first
                                    # of a one entry list
        if data['sponsor1']['email']:
            data['cc'].append(data['sponsor1']['email'])
        data['sponsor2'] = make_dict(sponsor_keys.split(),
                fetch(query.format(data['sponsor2']),
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

def add_sponsor_cc2data(data):
    """
    <data> must be a dict with sponsor1 and sponsor1 keys
    who's values are personIDs. 
    A data['cc'] entry is created as a string with sponsor
    emails separated by commas. The string could be empty
    if sponsors don't have email.
    """
    query = """SELECT last, first, suffix, email FROM People
            WHERE personID = {};"""  # returns a one entry list
    sponsor_keys = "last first suffix email"
    data['cc'] = []
    for sponsor in ('sponsor1', 'sponsor2'):
        sponsor_dict = make_dict(sponsor_keys.split(),
            fetch(query.format(data[sponsor]),
                from_file=False)[0])  # '[0]' is to get first
                                    # of a one entry list
        if sponsor_dict['email']:
            data['cc'].append(sponsor_dict['email'])
    data['cc'] = ','.join(data['cc'])


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


def assign_welcome2full_membership(holder):
    ret = ['<welcome to full_membership mailing>',
            ]
    print("Create list of people to welcome as new member(s):")
    candidates = []
    while True:
        ids = id_by_name()
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
    # run a query to populate byID ==> holder.data2welcome
    byID = dict()
    for personID in candidates:
        tup = fetch('Sql/find_by_ID.sql',
                            params=(personID,))[0]
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'phone': tup[4],
                        'address': tup[5],
                        'town': tup[6],
                        'state': tup[7],
                        'postal_code': tup[8],
                        'country': tup[9],
                        'email': tup[10],
                        }
    if holder.cc_sponsors:
        for key, dic in byID.items():
            
            pass
    holder.working_data = byID
    return ret



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


if __name__ == '__main__':
#   print(get_sponsors(110))
#   exercise_get_person_fields_by_ID(146)
#   print("\nWhat follows are three statements:....")
#   print(get_statement(get_data4statement(197)))
#   print(get_statement(get_data4statement(42)))
#   print(get_statement(get_data4statement(157)))
#   exercise_getIDs_by_status(200)
#   exercise_assign_applicants2welcome()
    exercise_add_sponsor_cc2data()
