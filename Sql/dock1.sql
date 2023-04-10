/* Sql/dock1.sql */
/* in theory- could return an empty list */
SELECT P.personID, P.first, P.last, P.suffix, DP.cost
FROM People as P
JOIN Dock_Privileges as DP
ON P.personID = DP.personID
WHERE NOT DP.cost = 0;
