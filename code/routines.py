#!/usr/bin/env python3

# File: code/routines.py

import sqlite3

db_file_name = '/home/alex/Git/Sql/Secret/club.db'


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
    

def main():
    id_dict = get_people_fields_by_ID(
            db_file_name, ('first', 'last'))
    for key in id_dict.keys():
        print(f"{key}:  {id_dict[key]}")


if __name__ == '__main__':
    main()

