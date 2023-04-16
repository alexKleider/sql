#!/usr/bin/env python3

# File: enter.py

import sqlite3

schema = """
    ReceiptID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    date_received TEXT NOT NULL,
    dues INTEGER DEFAULT NULL,
    dock INTEGER DEFAULT NULL,
    kayak INTEGER DEFAULT NULL,
    mooring INTEGER DEFAULT NULL,
    acknowledged TEXT DEFAULT NULL
"""

def main():
    db_file_name = '/home/alex/Git/Sql/Secret/club.db'
    db = sqlite3.connect(db_file_name)
    cursor = db.cursor()
    data = {"personID": 119,
            "date_received": "20230407",
            "dues": 50,
            "dock": 0,
            "kayak": 0,
            "mooring": 0,
            "acknowledged": "20230410",
            }
    f_keys = ", ".join([key for key in data.keys()])
    f_values = ", ".join([repr(value) for value in data.values()])
    query = ("INSERT INTO Receipts ({}) VALUES ({});"
                    .format(f_keys, f_values))
    print(query)
    cursor.execute(query, data)
    cursor.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
