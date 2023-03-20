#!/usr/bin/env python3

# File: alchemy.py

"""
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

# print(sqlalchemy.__version__)

query = "SELECT statusID, key, text FROM Stati;"


def getting(engine, query, dic=None):
    with engine.connect() as con:
        if dic:
            result = con.execute(sqlalchemy.text(query, dic))
        else:
            result = con.execute(sqlalchemy.text(query))
        return result.mappings()


def setting(engine, query, dic=None):
    with engine.connect() as con:
        if dic:
            result = con.execute(sqlalchemy.text(query), dic)
        else:
            result = con.execute(sqlalchemy.text(query))
        con.commit()

def task1():
    for entry in getting(engine, query):
        for key in entry.keys():
            print(f"{entry[key]:<12}",end='')
        print()
#   con.commit()  # needed if changing (vs querying) data

def task2():
    insert_query = """
    /* Sql/insert_date.sql */
    UPDATE Applicants
    SET (meeting, ) VALUES (:meeting, )
    WHERE personID = :personID
    ;
    """
    params = {'meeting': '230303',
        'personID': 143,
        }
    setting(engine, insert_query, dic=params) 


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(
        "sqlite+pysqlite:////home/alex/Git/Sql/Secret/club.db"
#       , echo=True
        )
    task2()
