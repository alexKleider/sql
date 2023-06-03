/* Sql/dues_by_ID.sql */
-- returns an empty list if no entry in the dues table
-- needs an ID inserted
SELECT P.personID, D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
WHERE p.personID = ?;
