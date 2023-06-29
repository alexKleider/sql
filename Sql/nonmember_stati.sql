/* Sql/nonmember_stati.sql */
SELECT P.first, P.last, P.personID, P.suffix, PS.begin, S.text, PS.end
FROM People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON S.statusID = PS.statusID
WHERE S.key NOT IN ('m')
AND PS.end < '20230630'
-- AND NOT S.key LIKE 'z%'
;

