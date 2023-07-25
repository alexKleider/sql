/* Sql/id_from_names_fff.sql */
/* this one includes suffix field */
SELECT personID from People 
WHERE first = "{first}"
AND last = "{last}"
AND suffix = "{suffix}";
