#!/usr/bin/env python3

# File: main.py

import sqlite3
import add_data

db_file_name = "Sanitized/club.db"
db_file_name = "Secret/club.db"

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


def get_people_fields_by_ID(fields):
    """
    Return the field values by PersonID in the People table.
    """
    ret = {}
    query = """SELECT * FROM People;"""
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, query)
    res = cur.fetchall()
    for entry in res:
        ret[entry[0]] = entry[1:]
    return ret
    

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
    id_dict = get_people_fields_by_ID(())
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, """
SELECT statusID, key FROM Stati WHERE key LIKE 'a%';
""")
    res = cur.fetchall()
    _ = input(f"{res}")
    applicant_dict = {}
    for key, code in res:
        applicant_dict[code] = [key, ]
#   _ = input(f"applicant_dict: {applicant_dict}")
    for key in applicant_dict.keys():
        execute(cur,con, """SELECT personID
            FROM Person_Status WHERE statusID = "{}";
            """.format(applicant_dict[key][0]))
        res = cur.fetchall()
        if res:
            for r in res:  # r[0] is personID
                print(f"{r[0]}:  {id_dict[r[0]]}")
#               applicant_dict[key].append(r[0])
#               print(applicant_dict[key])


    return
    for ID in IDs:
        print(f"res of query_b: {repr(res)}")
    if res:
        ids = [item[0] for item in res]
        for personID in ids:
            execute(cur,con,query_c.format(personID))
            res = cur.fetchall()
            print(f"res of query_c: {repr(res)}")
            if res:
                first, last = res[0]
                print(first, last)


if __name__ == '__main__':
    main()
    
