/* Sql/find.sql */
/* Find ID based on partial first and/or last name(s). */
    SELECT personID, first, last, suffix
    FROM People
    WHERE first LIKE ? OR last LIKE ?
    ;
