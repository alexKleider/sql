/* Sql/q2.sql */

SELECT 
    People.personID, first, last, Stati.text, Stati.key
FROM People, Person_Status, Stati
    WHERE
        Person_Status.personID = People.personID 
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = 'aw'
    ;
