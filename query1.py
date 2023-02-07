#!/usr/bin/env python3

# File: query1.py

import sqlite3

db_file_name = "Sanitized/club.db"
query = """
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People, Person_Status, Stati
    WHERE Person_Status.personID = People.personID 
    AND Person_Status.statusID = (SELECT statusID  
        FROM Stati WHERE key = 'aw')
    ;
-- the above prints many lines only one of which
-- is the one wanted!  
"""
query = """
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People, Person_Status, Stati
    WHERE Person_Status.personID = People.personID 
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = 'aw'
    ;
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
    print(query)
    print()
    execute(cur, con, query)
#   print(cur.fetchall())
    for sequence in cur.fetchall():
        print(sequence)
        if sequence[-1] == 'aw':
            print('\t{}'.format(sequence))



if __name__ == '__main__':
    main()
