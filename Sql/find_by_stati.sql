/* Sql/find_by_stati.sql */

SELECT 
    People.personID, first, last, Stati.text, Stati.key
FROM People, Person_Status, Stati
    WHERE
        Person_Status.personID = People.personID 
    AND Person_Status.statusID = Stati.statusID
    AND Stati.key = ?
    ;
/*
(35, 'Ralph', 'Camiccia', 'Director- term ends Feb next odd year', 'z5_d_odd')
(70, 'Rudi', 'Ferris', 'Director- term ends Feb next odd year', 'z5_d_odd')
(135, 'Jeff', 'McPhail', 'Director- term ends Feb next odd year', 'z5_d_odd')
(144, 'Don', 'Murch', 'Director- term ends Feb next odd year', 'z5_d_odd')
*/
