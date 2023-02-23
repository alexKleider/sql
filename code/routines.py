#!/usr/bin/env python3

# File: code/routines.py

"""
Contains some 'helper' code to support data base management.
"""

import sqlite3

db_file_name = '/home/alex/Git/Sql/Secret/club.db'


def make_dict(keys, values):
    """
    Parameters are iterables of equal length.
    A dict is returned.
    """
    ret = {}
    for key, value in zip(keys, values):
        ret[key] = value
    return ret


def execute_from_file(sql_file,
        db=db_file_name,
        params=None, commit=False):
    connection = sqlite.connection(db)
    cursor = connection.cursor()
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
    ret = cursor.fetchall()
    if commit:
        connection.commit()
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
    connection.commit()


def get_ids_by_name(cur, con, first, last):
    """
    Returns People.personID (could be more than one!)
    for anyone with <first> <last> name.
    Returns a (possible empty) tuple.
    Unlikely it'll ever be more than a tuple with one value
    """
    query = f"""SELECT personID from People
            WHERE People.first = "{first}"
            AND People.last = "{last}" """
#   _ = input(query)
    execute(cur, con, query)
    res = cur.fetchall()
    res= [item[0] for item in res]
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
            or (len(line) == 1)):
                continue
            command.append(line)
            if line.endswith(';'):
                yield ' '.join(command)
                command = []


def fetch(query_source, db_file_name=db_file_name):
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con,
            get_query(query_source))
    return cur.fetchall()


def exercise_get_people_fields_by_ID():
    id_dict = get_people_fields_by_ID(
            db_file_name, ('first', 'last'))
    for key in id_dict.keys():
        print(f"{key}:  {id_dict[key]}")


if __name__ == '__main__':
#   exercise_get_people_fields_by_ID()
    pass

