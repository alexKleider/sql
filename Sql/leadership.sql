
/* File: leadership.sql */

SELECT P.personID, P.first, P.last, S.text, PS.begin, PS.end
FROM People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON S.statusID = PS.statusID
WHERE S.statusID in (20, 21, 22, 23, 24, 25)
--ORDER BY P.last
ORDER BY S.statusID
;
