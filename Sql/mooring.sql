/* Sql/mooring.sql */
/* in theory- could return an empty list */
-- Schema has changes since this was created...
-- you might want M.owing rather than mooring_cost
SELECT P.personID, M.mooring_cost
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
WHERE NOT M.mooring_cost = 0;
