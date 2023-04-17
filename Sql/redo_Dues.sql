/* Sql/redo_Dues.sql */
-- follow this with old2new_Dues.py

DROP TABLE IF EXISTS Dues;
CREATE TABLE Dues ( -- AS D
    personID INTEGER PRIMARY KEY,
    --be sure and insert a value!
    --otherwise, will autoincriment!
    --no one will pay for >1 
    --so no need for an
    --auto generated PRIMARY KEY
    dues_owed NUMERIC DEFAULT 200
    );
