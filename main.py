#!/usr/bin/env python3

# File: main.py

import sqlite3
import add_data

db_file_name = "Sanitized/club.db"

query_a = """
SELECT statusID FROM Stati WHERE key = 'aw';
"""

query_b = """
SELECT personID FROM Person_Status WHERE statusID = {};
"""

query_c = """
SELECT first, last FROM People WHERE personID = {};
"""

query_get_nothing = """
SELECT Person_Status.personID, Person_Status.statusID
    FROM Person_Status
    JOIN Stati
        on Stati.statusID = 'aw'
;"""

query_1 = """
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People
    LEFT JOIN Person_Status
        ON People.personID = Person_Status.personID
    LEFT JOIN Stati
        ON Person_Status.personID = Stati.statusID
;"""


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
#   _ = input(command)
    connection.commit()


def main():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, query_a)
    res = cur.fetchall()
    statusID = res[0][0]
    execute(cur,con,query_b.format(statusID))
    res = cur.fetchall()
    personID = res[0][0]
    execute(cur,con,query_c.format(personID))
    res = cur.fetchall()
    first, last = res[0]
    print(first, last)


if __name__ == '__main__':
    main()
