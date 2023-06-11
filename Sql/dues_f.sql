/* Sql/dues_f.sql */
/* includes only those who have not paid */
SELECT P.personID, D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID = 15 and PS.end < {}
AND NOT D.dues_owed = 0;
;
