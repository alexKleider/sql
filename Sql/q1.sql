/* Sql/q1.sql */

SELECT People.personID, first, last, Stati.text, Stati.key
    FROM People, Person_Status, Stati
    WHERE Person_Status.personID = People.personID 
    AND Person_Status.statusID = (SELECT statusID  
        FROM Stati WHERE key = 'aw')
    ;
-- the above prints many lines only one of which
-- is the one wanted!  
