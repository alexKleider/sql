#!/usr/bin/env python3

# File: alchemy.py

"""
Use this module when wanting a list of dicts
(rather than a list of tuples)
in response to a query.

# getting:
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
# execute many...
# setting
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()
"""

import sqlalchemy

try: from code import club
except ImportError: import club

# print(sqlalchemy.__version__)

AlchemyDB = "sqlite+pysqlite:///" + club.DB

query = "SELECT statusID, key, text FROM Stati;"


def getting(query, dic=None):
    engine = sqlalchemy.create_engine(AlchemyDB
#       , echo=True
        )
    with engine.connect() as con:
        if dic:
            result = con.execute(sqlalchemy.text(query, dic))
        else:
            result = con.execute(sqlalchemy.text(query))
        return result.mappings()


def setting(query, dic=None):
    engine = sqlalchemy.create_engine(AlchemyDB
#       , echo=True
        )
    with engine.connect() as con:
        if dic:
            result = con.execute(sqlalchemy.text(query), dic)
        else:
            result = con.execute(sqlalchemy.text(query))
        con.commit()

def task1():
    query = "SELECT statusID, key, text FROM Stati;"
    for entry in getting(query):
        for key in entry.keys():
            print(f"{entry[key]:<12}",end='')
        print()
#   con.commit()  # needed if changing (vs querying) data

def task2():
    insert_query = """
    /* Sql/insert_date.sql */
    UPDATE Applicants
    SET meeting3 = :meeting3 
    WHERE personID = :personID
    ;
    """
    params = {'meeting3': '230303',
        'personID': 143,
        }
    setting(insert_query, dic=params) 

def get_dues():
    query = """
    SELECT personID, dues_owed FROM Dues;
    """
    return getting(query)

def show_dues_owing():
    for d in get_dues():
        print(f"{repr(d)}")

def get_dock_fees_owed():
    query = """
    SELECT personID, cost FROM Dock_Privileges;
    """
    return getting(query)

def show_dock_fees_owed():
    for d in get_dock_fees_owed():
        print(f"{repr(d)}")

def get_kayak_fees_owed():
    query = """
    SELECT personID, slot_cost FROM Kayak_Slots;
    """
    return getting(query)

def show_kayak_fees_owed():
    for d in get_kayak_fees_owed():
        print(f"{repr(d)}")

def get_mooring_fees_owed():
    query = """
    SELECT personID, mooring_cost FROM Moorings;
    """
    return getting(query)

def show_mooring_fees_owed():
    for d in get_mooring_fees_owed():
        print(f"{repr(d)}")

if __name__ == '__main__':
    show_dues_owing()
    _ = input()
    show_dock_fees_owed()
    _ = input()
    show_kayak_fees_owed()
    _ = input()
    show_mooring_fees_owed()

#   task1()
