/* Sql/kayak1.sql */
/* in theory- could return an empty list */
SELECT P.personID, P.first, P.last, P.suffix,
--         0          1         2      3
        K.slot_code, K.slot_cost
--         4             5
FROM People as P
JOIN Kayak_Slots as K
ON P.personID = K.personID
WHERE NOT K.slot_cost = 0;
