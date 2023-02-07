#!/usr/bin/env python3

# File: query2.py

import sqlite3

db_file_name = "Sanitized/club.db"

q2 = """
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People
    INNER JOIN Person_Status
        ON People.personID = Person_Status.personID
    INNER JOIN Stati
        ON Person_Status.personID = Stati.statusID
        AND Stati.key = 'aw'
    ;
-- this query gives the wrong answer!! No idea why.
"""


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
    connection.commit()


def main():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    print(q2)
    print()
    execute(cur, con, q2)
#   print(cur.fetchall())
    for sequence in cur.fetchall():
        print(sequence)
        if sequence[-1] == 'aw':
            print(f'\t{sequence}')



if __name__ == '__main__':
    main()
