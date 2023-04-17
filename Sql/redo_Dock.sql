
/* Sql/redo_Dock.sql */
/* Drops and re-does set up of the 
    Dock_Privileges table.
*/

DROP TABLE IF EXISTS Dock_Privileges;
CREATE TABLE Dock_Privileges ( -- AS Do
    personID INTEGER PRIMARY KEY,
    --be sure and insert a value!
    --otherwise, will autoincriment!
    --no one will pay for >1 
    --so no need for an
    --auto generated PRIMARY KEY
    cost NUMERIC DEFAULT 75
    );

