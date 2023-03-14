/* Sql/select_like.sql */
/* a 2 tuple parameter is required (remember '%'!)
    SELECT personID, first, last, suffix
    FROM People
    WHERE first LIKE ? OR last LIKE ?
    ;
