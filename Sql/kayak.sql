/* Sql/kayak.sql */
/* in theory- could return an empty list */
SELECT P.personID, K.slot_cost
FROM People as P
JOIN Kayak_Slots as K
ON P.personID = K.personID
WHERE NOT K.slot_cost = 0;
