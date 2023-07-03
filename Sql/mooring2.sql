/* Sql.mooring2.sql */
/* Provides the essential info re moorings. */
SELECT P.personID, P.first, P.last, M.mooring_code, M.mooring_cost, M.owing
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
ORDER BY P.last, P.first, P.suffix;
