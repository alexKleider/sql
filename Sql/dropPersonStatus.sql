/* Sql/dropPersonStatus.sql */
/* requires a 2 tuple (personID, statusID) */
-- the following works:
-- DELETE FROM Person_Status WHERE personID = 69 AND statusID = 25;
DELETE FROM Person_Status
WHERE personID = ? AND statusID = ?
;
