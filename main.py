#!/usr/bin/env python3

# File: main.py

import os
import sys
from code import routines

import sqlite3
db_file_name = "Sanitized/club.db"
db_file_name = "Secret/club.db"

query_1 = """
SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People
    LEFT JOIN Person_Status
        ON People.personID = Person_Status.personID
    LEFT JOIN Stati
        ON Person_Status.personID = Stati.statusID
;"""


def main():
    id_dict = routines.get_people_fields_by_ID(
            db_file_name, ('first', 'last'))
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query_statusIDs4applicants = """SELECT
        statusID, key FROM Stati WHERE key LIKE 'a%';"""
    routines.execute(cur, con, query_statusIDs4applicants)
    res = cur.fetchall()
#   _ = input(f"{res}")
    statusID_by_key = {}
    for statusID, key in res:
        statusID_by_key[key] = statusID
#   _ = input(f"statusID_by_key: {statusID_by_key}")
    keys = statusID_by_key.keys()
    print("KEY:  id list")
    print("====  =======")
    for key in keys:
        routines.execute(cur,con, """SELECT personID
            FROM Person_Status WHERE statusID = "{}";
            """.format(statusID_by_key[key]))
        res = cur.fetchall()
        if res:
            print(f"{key}: {[id_dict[entry[0]] for entry in res]}")


if __name__ == '__main__':
    main()
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query = """
        SELECT
            Stati.key,
            People.first, People.last
        FROM People
        JOIN Person_Status
            ON Person_Status.personID = People.personID
        JOIN Stati
            ON Stati.statusID = Person_Status.statusID
        WHERE
            Stati.key IN ("a-", "a" , "a0", "a1", "a2",
                "a3", "ai", "ad", "av", "aw", "am")
        ORDER BY Stati.key
    ;"""

    routines.execute(cur, con, query)
    res = cur.fetchall()
    print("\nSame but all with one query:")
    for item in res:
        print(item)
    
