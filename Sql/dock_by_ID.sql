/* Sql/dock_by_ID.sql */
-- returns an empty list if not a dock user
-- needs an ID inserted
SELECT P.personID, DP.cost
FROM People as P
JOIN Dock_Privileges as DP
ON P.personID = DP.personID
WHERE p.personID = ?;
