/* Sql/dues0.sql */
/* revising query to collect dues & fees outstanding */
/* includes people who have paid */
SELECT P.personID, D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
-- WHERE NOT D.dues_owed = 0
;
