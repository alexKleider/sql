/* Sql/dues_f.sql */
/* includes only those still owing */
SELECT P.personID, D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID = 15
AND PS.end < {}
AND D.dues_owed > 0
;
