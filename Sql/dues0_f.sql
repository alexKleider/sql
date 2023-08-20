/* Sql/dues0_f.sql */
/* includes people who have paid */
SELECT P.personID, D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID in (8, 11, 15)
AND (PS.end = '' OR PS.end < {})
;
