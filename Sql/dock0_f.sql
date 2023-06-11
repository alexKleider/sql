/* Sql/dock0_f.sql */
SELECT P.personID, DP.cost
FROM People as P
JOIN Dock_Privileges as DP
ON P.personID = DP.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID = 15 
AND PS.end < {}
;
