/* Sql/q3.sql */

SELECT Stati.key, first, last, Stati.text
FROM
    People, Person_Status, Stati
WHERE
    Person_Status.personID = People.personID 
AND Person_Status.statusID = Stati.statusID
AND Stati.key = '{}'
    ;
