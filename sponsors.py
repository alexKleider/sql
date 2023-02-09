#!/usr/bin/env python3

# File: sponsors.py

import sqlite3

db_file_name = "Sanitized/club.db"
q1 = """
    SELECT * from Applicants 
    WHERE meeting2 = ''
    ;"""


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
    connection.commit()


def get_applicants():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur,con, q1)
    fetched = cur.fetchall()
#   print("Fetched:")
#   print(fetched)
    if fetched:
        for sequence in fetched:
            print(sequence)

if __name__ == '__main__':
    get_applicants()
