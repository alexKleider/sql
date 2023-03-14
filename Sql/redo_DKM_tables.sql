/* Sql/redo_DKM_tables.sql */

DROP TABLE IF EXISTS Dock_Privileges;
CREATE TABLE Dock_Privileges ( -- AS Do
    personID INTEGER NOT NULL UNIQUE,
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
    personID INTEGER
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
    personID INTEGER
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 mooring.
    );
