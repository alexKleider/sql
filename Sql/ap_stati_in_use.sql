/* Sql/ap_stati_in_use.sql */
SELECT P.personID, P.first, P.last, P.suffix, S.statusID, S.key
FROM People AS P
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati AS S
ON PS.statusID = S.statusID
WHERE S.key LIKE  'a%'
ORDER BY S.key
;
