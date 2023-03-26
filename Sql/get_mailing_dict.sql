/* Sql/get_mailing_dict.sql*/
/* requires a one tuple param: a personID */
/* in theory- could return an empty list */
SELECT first, last, suffix,
    address, town, state, postal_code, country
FROM People
WHERE personID = ?;
