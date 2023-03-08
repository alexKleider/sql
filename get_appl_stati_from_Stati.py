#!/usr/bin/env python3

# File: get_appl_stati_from_Stati.py

import sqlite3

dbpath = "/home/alex/Git/Sql/Secret/"
club_db = "club.db"

query = "Sql/get_appl_stati_from_Stati.sql"

def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("theClub")
    """
    try:
        db = sqlite3.connect(path)
        theClub = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:",
                path)
        db, theClub = None, None
        raise
    return db, theClub

def try_query(cursor, query):
    try:
        cursor.execute(query)
        ret = cursor.fetchall()
    except sqlite3.OperationalError:
        print(f"The following query failed:\n{query}\n======")
        return None
        raise
    return ret

def closeDB(database, theClub):
    try:
       theClub.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise
       

def main():
    with open(query, 'r') as infile:
        q = infile.read()
    db, cur = initDB(dbpath+club_db)
    ret = try_query(cur, q)
    for line in ret:
        print(line)

if __name__ == '__main__':
    main()
