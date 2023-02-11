-- File: create_tables.sql
-- Suggest use club.db
-- parsed by add_data.py to set up tables
-- see associated specifications.txt file

DROP TABLE IF EXISTS People;
CREATE TABLE People (
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
CREATE TABLE Applicants (
    applicantID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL UNIQUE,
        --foreign key
    app_rcvd TEXT NOT NULL,
    fee_rcvd TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    inducted TEXT DEFAULT '',
    dues_paid TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Sponsors;
--intersection table
CREATE TABLE Sponsors (
    personID INTEGER NOT NULL,
        --foreign key
    sponsorID INTEGER NOT NULL
        --foreign key
    );

DROP TABLE IF EXISTS Stati;
CREATE TABLE Stati (
    statusID INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    text TEXT NOT NULL
    );

DROP TABLE IF EXISTS Person_Status;
--intersection table
CREATE TABLE Person_Status (
    personID INTEGER NOT NULL,
    statusID INTEGER NOT NULL
    );

DROP TABLE IF EXISTS Attrition;
--keeping data in People table
CREATE TABLE Attrition (
    attritionID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
        --foreign key
    date TEXT DEFAULT '',
    reason TEXT DEFAULT ''
    );

DROP TABLE IF EXISTS Dues;
CREATE TABLE Dues (
    personID INTEGER UNIQUE NOT NULL,
        --foreign key
    dues_owed NUMERIC DEFAULT 100
    );

DROP TABLE IF EXISTS Dock_Privileges;
CREATE TABLE Dock_Privileges (
    personID TEXT NOT NULL UNIQUE,
    --no one will pay for >1 
    --so no need for an
    --auto generated PRIMARY KEY
    cost NUMERIC DEFAULT 75
    );

DROP TABLE IF EXISTS Kayak_Slots;
CREATE TABLE Kayak_Slots (
    slotID INTEGER PRIMARY KEY,
    personID TEXT,
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 kayak slot.
    slot_code TEXT NOT NULL UNIQUE,
    slot_cost NUMERIC DEFAULT 70
    );

DROP TABLE IF EXISTS Moorings;
CREATE TABLE Moorings (
    mooringID INTEGER PRIMARY KEY,
    personID TEXT,
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 mooring.
    mooring_code TEXT NOT NULL UNIQUE,
    mooring_cost NUMERIC DEFAULT 0
    );

