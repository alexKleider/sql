/* Sql/get_status_ID.sql */
/* requires an argument (the status key) as a one tuple */
SELECT    statusID
FROM Stati
WHERE key = ? ;
