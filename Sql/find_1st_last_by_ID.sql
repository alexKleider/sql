/* Sql/find_1st_last_by_ID.sql */
/* Find first, last, suffix info based on personID . */
    SELECT first, last, suffix 
    FROM People
    WHERE personID = ?
    ;
