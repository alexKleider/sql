/* Sql/get_appl_stati_from_Stati.sql */
SELECT S.key, P.personID, P.first, P.last, P.suffix 
FROM People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON S.statusID = PS.statusID
AND S.key LIKE 'a%'
ORDER BY S.key
;
