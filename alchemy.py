#!/usr/bin/env python3

# File: alchemy.py

import sqlalchemy

# print(sqlalchemy.__version__)

engine = sqlalchemy.create_engine(
        "sqlite+pysqlite:////home/alex/Git/Sql/Secret/club.db"
#       , echo=True
        )
with engine.connect() as con:
    result = con.execute(sqlalchemy.text(
        "SELECT statusID, key, text FROM Stati"))
    for row in result:
        print(f'{row.statusID:>3}: {row.key:<12} {row.text}')
#   con.commit()  # needed if changing (vs querying) data
