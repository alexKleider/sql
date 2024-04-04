/* Sql/nonmember_stati_f.sql */
SELECT P.personID, P.first, P.last, P.suffix,
        PS.begin, S.text, PS.end
FROM People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON S.statusID = PS.statusID
WHERE S.key NOT IN ('am', 'm')
AND 
    (PS.begin = "" OR PS.begin < {})
AND
    (PS.end = "" OR PS.end > {})
ORDER BY P.last, P.first
;

