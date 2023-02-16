#!/usr/bin/env python3

# File: show.py

import sqlite3
from code import routines

db_file_name = "Secret/club.db"
query_source = "Sql/show.sql"


with open(query_source, 'r') as inf:
    query = inf.read()

def main():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    routines.execute(cur, con, query)
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
    print('\n'.join(report))


if __name__ == '__main__':
    main()
