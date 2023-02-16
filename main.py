#!/usr/bin/env python3

# File: main.py

"""
Main driver of SQL version of
             the
    Bolinas Rod & Boat Club
          Membership
data management software.
"""

import sys
import sqlite3
from code import routines

db_file_name = "Secret/club.db"


def get_query(sql_source_file):
    with open(sql_source_file, 'r') as source:
        return source.read()


def show_cmd():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    routines.execute(cur, con,
            get_query('Sql/show.sql'))
    res = cur.fetchall()
    n = len(res)
    _ = input(f"Number of members: {n}\n")
    report = ["""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS ROD &
BOAT CLUB MEMBERSHIP CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED
FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BOARD OF THE BRBC.
""", ]
    first_letter = 'A'
    for item in res:
        last_initial = item[1][:1]
        if last_initial != first_letter:
            first_letter = last_initial
            report.append("")
        report.append(
        "{}, {} [{}] {}, {}, {} {} [{}]".format(*item))
    return('\n'.join(report))


def get_command():
    choice = input("""Choose one of the following:
0. Exit
1. Show
2. Not implemented
...... """)
    if choice == '0': sys.exit()
    elif choice == '1': return show_cmd
    elif choice == '2': print("Not implemented")
    else: print("Not implemented")


if __name__ == '__main__':
    cmd = None
    largs = len(sys.argv)
    if largs > 1:
        cmd = sys.argv[1]
        if cmd == 'show': cmd = show_cmd
        else: cmd = None
    else: 
        cmd = get_command()
    if cmd: 
        res = cmd()
        outfile = input("Send result to file: ")
        with open(outfile, 'w') as outstream:
            outstream.write(res)

