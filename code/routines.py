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


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
#   _ = input(command)
    connection.commit()


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


def fetch(query_source, db_file_name=db_file_name):
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con,
            get_query(query_source))
    return cur.fetchall()


def main():
    id_dict = get_people_fields_by_ID(
            db_file_name, ('first', 'last'))
    for key in id_dict.keys():
        print(f"{key}:  {id_dict[key]}")


if __name__ == '__main__':
    main()

