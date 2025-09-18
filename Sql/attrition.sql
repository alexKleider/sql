/*
    File: attrition.sql
*/

SELECT P.personID, P.first, P.last, P.suffix, S.key, PS.begin 
FROM People as P
JOIN Person_Status as PS
    ON P.personID = PS.personID
JOIN Stati as S
    ON PS.statusID = S.statusID
WHERE (PS.end = ""
    AND
       S.statusID in (18, 27, 28)
/* terminated, no longer a member, died recently */
        )
    ORDER BY PS.begin
    ;

