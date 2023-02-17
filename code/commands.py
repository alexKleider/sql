#!/usr/bin/env python3

# File: code/commands.py

"""

"""

import sqlite3
from code import routines

db_file_name = "Secret/club.db"


def get_command():
    choice = input("""Choose one of the following:
0. Exit
1. Show
2. Not implemented
...... """)
    if choice == '0': sys.exit()
    elif choice == '1': return show_cmd
    elif choice == '2': return appl_cmd
    elif choice == '3': print("Not implemented")
    else: print("Not implemented")


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
    routines.execute(cur, con,
            get_query(query_source))
    return cur.fetchall()


def show_cmd():
    res = fetch('Sql/show.sql')
    n = len(res)
#   _ = input(f"Number of members: {n}\n")
    report = [f"""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS ROD &
BOAT CLUB MEMBERSHIP CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED
FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BOARD OF THE BRBC.

There are currently {n} members in good standing:
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


def appl_cmd():
    pass
