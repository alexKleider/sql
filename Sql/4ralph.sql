/* 4ralph.sql */
/* should be deleted or the "221231" date changed to something rational! */
SELECT P.first, P.last, S.text, PS.begin, PS.end from People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON PS.statusID = S.statusID
WHERE S.statusID = 15
AND PS.begin > 221231;

