/* Sql/redo_Kayak.sql */
/* Drops and re-does set up of the 
    Kayak_Slots table.
*/

DROP TABLE IF EXISTS Kayak_Slots;
CREATE TABLE Kayak_Slots ( -- AS K
    slot_code TEXT PRIMARY KEY,
    personID INTEGER,
    -- foreign key
    -- unlikely but theoretically 
    -- possible for one member to
    -- have >1 kayak slot.
    slot_cost NUMERIC DEFAULT 100
    );

