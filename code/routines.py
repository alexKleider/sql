#!/usr/bin/env python3

# File: code/routines.py

"""
Contains some 'helper' code to support data base management.
"""

import sqlite3

db_file_name = '/home/alex/Git/Sql/Secret/club.db'


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
    else:
        if params:
#           _ = input(f"params set to '{params}'")
            cur.execute(query, params)
        else:
            cur.execute(query)
#   _ = input(
#       f"get_query_result returning the following:\n {ret}")
    ret = cur.fetchall()
    closeDB(db, cur)
    return ret


def make_dict(keys, values):
    """
    Parameters are iterables of equal length.
    A dict is returned.
    """
    ret = {}
    for key, value in zip(keys, values):
        ret[key] = value
    return ret


def get_query(sql_source_file, values=None):
    """
    Reads a query from a file with option to bind values 
    to place holders.
    If <values> is provided: it must consist of either
    a sequence of length to match number of qmark placeholders
    or a dict containing all keys needed for named placeholders
    each of which is prefaced by a colon. eg: (:key1, :key2).
    """
    with open(sql_source_file, 'r') as source:
        ret = source.read()
        if values:
            ret = ret.format(*formatting)
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


def get_people_fields_by_ID(db_file_name, fields=None):
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
    

def get_query(sql_source_file, formatting=None):
    """
    Reads a query from a file.
    If <formatting> is provided: must consist of sequence of
    length to match number of fields to be formatted.
    """
    with open(sql_source_file, 'r') as source:
        ret = source.read()
        if formatting:
            ret = ret.format(*formatting)
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


def exercise_get_people_fields_by_ID():
    id_dict = get_people_fields_by_ID(
            db_file_name, ('first', 'last'))
    for key in id_dict.keys():
        print(f"{key}:  {id_dict[key]}")


if __name__ == '__main__':
    exercise_get_people_fields_by_ID()
    pass

