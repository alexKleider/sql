-- File: create_tables.sql
-- Suggest use club.db
-- parsed by add_data.py to set up tables
-- see associated specifications.txt file

DROP TABLE IF EXISTS People;
CREATE TABLE People ( -- AS P
    personID INTEGER PRIMARY KEY,
    first TEXT NOT NULL,
    last TEXT NOT NULL,
    suffix TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    town TEXT DEFAULT '',
    state TEXT DEFAULT '',
    postal_code TEXT DEFAULT '',
    country TEXT DEFAULT 'USA',
    email TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Applicants;
-- also in Stati table
-- unitil > member
CREATE TABLE Applicants ( -- AS Ap
    applicantID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL UNIQUE,
        --foreign key
    sponsor1 TEXT DEFAULT '',
    sponsor2 TEXT DEFAULT '',
    app_rcvd TEXT NOT NULL,
    fee_rcvd TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    inducted TEXT DEFAULT '',
    dues_paid TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Stati;
CREATE TABLE Stati ( -- AS St
    statusID INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    text TEXT NOT NULL
    );

DROP TABLE IF EXISTS Person_Status;
--intersection table
CREATE TABLE Person_Status ( -- AS PS
    personID INTEGER NOT NULL,
    statusID INTEGER NOT NULL,
    PRIMARY Key (personID, statusID)
    -- composite primary key
    );

DROP TABLE IF EXISTS Attrition;
--keeping data in People table
CREATE TABLE Attrition ( -- AS At
    attritionID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    -- foreign key
    date TEXT DEFAULT '',
    reason TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Dues;
CREATE TABLE Dues ( -- AS Du
    personID INTEGER UNIQUE NOT NULL,
    -- foreign key
    -- only one entry per person
    dues_owed NUMERIC DEFAULT 100
    );

DROP TABLE IF EXISTS Dock_Privileges;
CREATE TABLE Dock_Privileges ( -- AS Do
    personID TEXT NOT NULL UNIQUE,
    --no one will pay for >1 
    --so no need for an
    --auto generated PRIMARY KEY
    cost NUMERIC DEFAULT 75
    );

DROP TABLE IF EXISTS Kayak_Slots;
CREATE TABLE Kayak_Slots ( -- AS K
    slotID INTEGER PRIMARY KEY,
    slot_code TEXT NOT NULL UNIQUE,
    slot_cost NUMERIC DEFAULT 70,
    personID TEXT
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 kayak slot.
    );

DROP TABLE IF EXISTS Moorings;
CREATE TABLE Moorings ( -- AS M
    mooringID INTEGER PRIMARY KEY,
    mooring_code TEXT NOT NULL UNIQUE,
    mooring_cost NUMERIC DEFAULT 0,
    personID TEXT
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 mooring.
    );

