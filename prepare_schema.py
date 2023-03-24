#!/usr/bin/env python3

# File: prepare_schema.py


# the following is output of .schema query for our database:
schema = """
CREATE TABLE People ( personID INTEGER PRIMARY KEY, first TEXT NOT NULL, last TEXT NOT NULL, suffix TEXT DEFAULT '', phone TEXT DEFAULT '', address TEXT DEFAULT '', town TEXT DEFAULT '', state TEXT DEFAULT '', postal_code TEXT DEFAULT '', country TEXT DEFAULT 'USA', email TEXT DEFAULT '' );
CREATE TABLE Applicants ( applicantID INTEGER PRIMARY KEY, personID INTEGER NOT NULL UNIQUE, sponsor1 TEXT DEFAULT '', sponsor2 TEXT DEFAULT '', app_rcvd TEXT NOT NULL, fee_rcvd TEXT DEFAULT '', meeting1 TEXT DEFAULT '', meeting2 TEXT DEFAULT '', meeting3 TEXT DEFAULT '', approved TEXT DEFAULT '', inducted TEXT DEFAULT '', dues_paid TEXT DEFAULT '' );
CREATE TABLE Stati ( statusID INTEGER PRIMARY KEY, key TEXT NOT NULL, text TEXT NOT NULL );
CREATE TABLE Person_Status ( personID INTEGER NOT NULL, statusID INTEGER NOT NULL, begin TEXT DEFAULT '', end TEXT DEFAULT '', PRIMARY Key (personID, statusID) );
CREATE TABLE Attrition ( attritionID INTEGER PRIMARY KEY, personID INTEGER NOT NULL, date TEXT DEFAULT '', reason TEXT DEFAULT '' );
CREATE TABLE Dues ( personID INTEGER UNIQUE NOT NULL, dues_owed NUMERIC DEFAULT 100 );
CREATE TABLE Dock_Privileges ( personID INTEGER NOT NULL UNIQUE, cost NUMERIC DEFAULT 75 );
CREATE TABLE Kayak_Slots ( slotID INTEGER PRIMARY KEY, slot_code TEXT NOT NULL UNIQUE, slot_cost NUMERIC DEFAULT 70, personID INTEGER );
CREATE TABLE Moorings ( mooringID INTEGER PRIMARY KEY, mooring_code TEXT NOT NULL UNIQUE, mooring_cost NUMERIC DEFAULT 0, personID INTEGER );
"""

schema = schema.split("\n")
ret = []
for line in schema:
    if not line: continue
    n = line.find(' ( ')
    ret.append(line[:n+3])
    parts = line[n+3:].split(', ')
    ret.append(',\n'.join(parts))
    ret.append('')
print('\n'.join(ret))
