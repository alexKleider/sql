/* Sql/select_like.sql */

    SELECT personID, first, last, suffix
    FROM People
    WHERE first LIKE ? OR last LIKE ?
    ;
