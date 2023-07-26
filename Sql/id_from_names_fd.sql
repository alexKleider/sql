/* Sql/id_from_names_fd.sql */
/* this one includes suffix field */
SELECT personID from People 
WHERE first = "{first}"
AND last = "{last}"
AND suffix = "{suffix}";
