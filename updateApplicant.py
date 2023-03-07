#!/usr/bin/env python3

# File: updateApplicant.py

"""
Seems not to be working.
May redact in favour of u_getAppl.py
"""

# set up the database and cursor
import sys
import sqlite3
from code import club
from code import routines

dbpath = "/home/alex/Git/Sql/Secret/"
club_db = "club.db"

def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("clubcursor")
    """
    try:
        db = sqlite3.connect(path+'club.db')
        clubcursor = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:",
                path)
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
 

def updateApplicant(cursor):
    with open("Sql/getApplicants.sql", 'r') as infile:
        query = infile.read()
    print(query)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.OperationalError: 
       print( "Sorry fixApplicants search failed" )
       raise
    else:
        if result:
            return result
        else: print("No matching data")
    return None


def fixApplicants(cur):
    applicants = getApplicants(cur)
    for appl in applicants:
        print(appl[0], ' ', appl[1:3], ' ', appl[-10:])
    


def main():
    print(f"Attempt to connect to {dbpath}")
    db, cur = initDB(dbpath)
    fixApplicants(cur)
    closeDB(db, cur)


if __name__ == '__main__':
    main()

