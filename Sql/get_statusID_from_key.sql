/* Sql/get_statusID_from_key.sql */
/* requires an argument (the status key) as a one tuple */
SELECT    statusID
FROM Stati
WHERE key = ? ;
