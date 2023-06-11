/* Sql/mooring0.sql */
SELECT P.personID, M.owing
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
;
