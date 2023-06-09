/* Sql/mooring_by_ID.sql */
-- returns an empty list if not a moorer
-- needs an ID inserted
SELECT P.personID, M.mooring_cost, M.owing
FROM People as P
JOIN Moorings as M
ON P.personID = M.personID
WHERE P.personID = ?;
