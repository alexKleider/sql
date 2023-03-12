#!/usr/bin/env python3

# File: main.py

"""
Main driver of SQL version of
             the
    Bolinas Rod & Boat Club
          Membership
data management software.
Support code found in the 'code' directory.
'code/routines.py' contains helper functions.
'code/commands.py': the commands themselves.

See code/commands/get_command() for what's so far implemented.

Some development is taking place in utilities.py
"""

import sys
import sqlite3
from code import commands

club_db = "/home/alex/Git/Sql/Secret/club.db"


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
 

if __name__ == '__main__':
    while True:
        cmd = commands.get_command()
        if cmd: 
            res = cmd()
            outfile = input(
            "Send result to file (blank if to StdOut:) ")
            if outfile:
                with open(outfile, 'w') as outstream:
                    outstream.write('\n'.join(res))
                    print(f"Results sent to {outstream.name}.")
            else:
                print("No file selected; output to stdout...")
                print('\n'.join(res))
        else:
            print("No valid command provided.")
        response = input(
            "\n Q)uit or any other key to continue... ")
        if response and response[0] in 'qQ': break 
