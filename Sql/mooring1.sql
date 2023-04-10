/* Sql/mooring1.sql */
/* in theory- could return an empty list */
SELECT P.personID, P.first, P.last, P.suffix,
--         0          1        2       3
        M.mooring_code, M.mooring_cost
--         4                  5
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
WHERE NOT M.mooring_cost = 0;
