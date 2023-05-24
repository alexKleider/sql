#!/usr/bin/env python3

# File: code/routines.py

"""
Contains some 'helper' code to support SQL(ite3)
relational data base management.
"""

import sqlite3
try: from code import club
except ImportError: import club

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
                    from_file=True, commit=False):
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
#   if commit:
#       db.commit()
#       _ = input("Committed!")
    closeDB(db, cur)
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


def make_dict(keys, values):
    """
    Parameters are iterables of equal length.
    A dict is returned.
    """
    assert len(keys) == len(values)
    ret = {}
    for key, value in zip(keys, values):
        ret[key] = value
    return ret


def get_menu_dict(items):
    """
    Returns a dict keyed by successive integers
    beginning with 1 (not zero!)
    """
    z = zip(range(1, len(items)+1), items)
    menu = dict()
    for key, item in z:
        menu[key] = item
    # remember: key is an int! (not a string)
    # '0' is reserved for Q)uit.
    return menu


def get_menu_response(items, header=None, incl0Q=True):
    """
    <items> a sequence of menu options
    <header>  line (if provided)to insert above the choices
    <incl0Q> == include a "0 to quit" 'choice'.
    It's up to client to deal with a "0 to quit" choice.
    Returns a 1 based integer
    """
    menu = get_menu_dict(items)  # see get_menu_dict doc_string
#   _ = input(menu)
    while True:
        if header: display = [header, ]
        else: display = []
        if incl0Q: display.append('  0: Q)uit')
        for key, value in menu.items():
            display.append(f"{key:>3}: {value}")
        print('\n'.join(display))
        response = int(input("Choice (must be an integer): "))
        if response>=0 and response<=(len(items)+1):
            return response




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
        _ = input(f"sponsorID: {sponsorID}")
        sponsors.append(fetch("""
        SELECT first, last, suffix, email FROM People
        WHERE personID = ?""",
        params=(sponsorID,), from_file=False))
    return sponsors


def get_data4statement(personID):
    """
    Returns a dict keyed by the following:
    personID, first, last, suffix,
    address, town, state, postal_code, country,
    email, dues_owed
    and if applicable:
    dock, kayak, mooring.
    """
    data = {'personID': personID,
            }
    res = fetch("Sql/dues_et_demographics_by_ID.sql",
            params=(personID, ) )[0]
#   print(res)
    data['first'] = res[0]
    data['last'] = res[1]
    data['suffix'] = res[2]
    data['address'] = res[3]
    data['town'] = res[4]
    data['state'] = res[5]
    data['postal_code'] = res[6]
    data['country'] = res[7]
    data['email'] = res[8]
    data['dues_owed'] = res[9]
    total = 0
    if data['dues_owed']: total += data['dues_owed']
    dock = fetch("Sql/dock_by_ID.sql",
            params=(personID, ) )
    if dock:
        data['dock'] = dock[0][1]
        total += data['dock']
    kayak = fetch("Sql/kayak_by_ID.sql",
            params=(personID, ) )
    if kayak:
        data['kayak'] = kayak[0][1] 
        total += data['kayak']
    mooring = fetch("Sql/mooring_by_ID.sql",
            params=(personID, ) )
#   _ = input(f"""mooring query ==> 
#   {repr(mooring)}
#           """)
    if mooring:
        data['mooring'] = mooring[0][1]
        total += data['mooring']
    data['total'] = total
#   for key, value in data.items():
#       print(f"{key}: {value}")
#   print()
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
    owing.append(    f"  Dues owing..... {data['dues_owed']:>3}")
    if "dock" in keys:
        owing.append(f"  Dock usage..... {data['dock']:>3}")
    if "kayak" in keys:
        owing.append(f"  Kayak storage.. {data['kayak']:>3}")
    if "mooring" in keys:
        owing.append(f"  Mooring fee.... {data['mooring']:>3}")
    owing.append(f"Total... ${data['total']}")
    return '\n'.join(owing)


def assign_owing(holder):
    """
    Assigns holder.working_data dict:
    Retrieve personID for each person who owes
    putting their relevant data into a dict keyed by ID.
    """
    byID = dict()
    # dues owing:
    for tup in (fetch("Sql/dues.sql")):
        byID[tup[0]] = {'first': tup[1],
                        'last': tup[2],
                        'suffix': tup[3],
                        'email': tup[4],
                        'address': tup[5],
                        'town': tup[6],
                        'state': tup[7],
                        'postal_code': tup[8],
                        'country': tup[9],
                        'dues_owed': tup[10],
                        }
    # dock privileges owing:
    for tup in fetch("Sql/dock.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['dock'] = tup[1]
    # kayak storage owing:
    for tup in fetch("Sql/kayak.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['kayak'] = tup[1]
    # mooring fee owing:
    for tup in fetch("Sql/mooring.sql"):
        _ = byID.setdefault(tup[0], {})
        byID[tup[0]]['mooring'] = tup[1]
    # save what's been collected...
    holder.working_data = byID


def assign_inductees4payment(holder):
    """
    Assigns holder.working_data dict keyed by ID pertaining
    to those recently inducted and yet to be notified.
    """
    byID = dict()
    res = fetch('Sql/inducted.sql')
    keys = ("personID last first suffix phone address town state"
    + " postal_code email sponsor1 sponsor2 begin end")
    keys = keys.split()
    query = """SELECT last, first, suffix, email FROM People
                WHERE personID = {};"""
    sponsor_keys = "last first suffix email"
    for line in res:
        data = make_dict(keys[1:],
                line[1:])
        data['cc'] = []
        data['sponsor1'] = make_dict(sponsor_keys.split(),
                fetch(query.format(data['sponsor1']),
                from_file=False)[0])
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
    res = get_person_fields_by_ID(id_n,
            fields = ('first', 'last', 'suffix'))
    print(res)


if __name__ == '__main__':
#   print(get_sponsors(110))
    exercise_get_person_fields_by_ID(146)
    print("\nWhat follows are three statements:....")
    print(get_statement(get_data4statement(197)))
    print(get_statement(get_data4statement(42)))
    print(get_statement(get_data4statement(157)))
    pass

