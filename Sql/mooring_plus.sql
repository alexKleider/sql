/* Sql/mooring_plus.sql */
/* in theory- could return an empty list */
SELECT P.personID, P.first, P.last, P.suffix,
        M.mooring_code, M.mooring_cost
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
WHERE NOT M.mooring_cost = 0;
