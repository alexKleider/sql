#!/usr/bin/env python3

# File: alchemy.py

"""
https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html
"""

import sqlalchemy as alch

engine = alch.create_engine("sqlite+pysqlite:///:memory:", echo=True)
with engine.connect() as conn:
    result = conn.execute(alch.text("select 'hello world'"))
    print(f"result.all(): '{result.all()}'")

