/* Sql/mooring0_f.sql */
SELECT P.personID, M.owing
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID = 15 and PS.end < {}
;
