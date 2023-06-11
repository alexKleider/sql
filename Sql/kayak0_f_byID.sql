/* Sql/kayak0_f_byID.sql */
/* includes paid up accounts */
-- must be formatted twice:
-- once with helpers.sixdigitdate
-- & 2nd time with personID
SELECT KS.slot_cost
FROM Kayak_Slots as KS
JOIN Person_Status as PS
ON KS.personID = PS.personID
WHERE PS.statusID IN (11, 15) 
AND PS.end < {}
AND KS.personID = {{}}
;
