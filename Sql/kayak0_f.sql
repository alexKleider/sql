/* Sql/kayak0_f.sql */
/* in theory- could return an empty list */
/* returns all, even those who have paid */
SELECT P.personID, K.slot_cost
FROM People as P
JOIN Kayak_Slots as K
ON P.personID = K.personID
JOIN Person_Status as PS
ON P.personID = PS.personID
WHERE PS.statusID = 15 and PS.end < {}
;
