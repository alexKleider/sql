/* Sql/find_by_status_key.sql */
/* requires a 1 tuple: Stati.key */
SELECT 
    People.personID, first, last, Stati.text, Stati.key
FROM People, Person_Status, Stati
    WHERE
        Person_Status.personID = People.personID 
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = ?
    ;
