/* Sql/ids_by_status_ff.sql */
SELECT personID
FROM Person_Status
WHERE statusID = {}
AND ((end > {}) OR (end = ''))
;
