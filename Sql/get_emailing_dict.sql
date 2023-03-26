/* Sql/get_emailing_dict.sql*/
/* requires a one tuple param: a personID */
/* in theory- could return an empty list */
SELECT first, last, suffix, email
FROM People
WHERE personID = ?
AND NOT email = '';
