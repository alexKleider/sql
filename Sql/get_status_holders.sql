/* Sql/get_status_holders.sql */
-- requires a one tuple, Stati.key, param.
SELECT People.personID, first, last, Stati.text, Stati.key
FROM People, Person_Status, Stati
    WHERE Person_Status.personID = People.personID 
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = ?
    ;
