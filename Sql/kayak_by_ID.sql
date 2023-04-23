/* Sql/kayak_by_id.sql */
-- returns an empty list if not a kayak storer
-- needs an ID inserted
SELECT P.personID, K.slot_cost
FROM People as P
JOIN Kayak_Slots as K
ON P.personID = K.personID
WHERE p.personID = ?;
