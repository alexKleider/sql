/* Sql/kayak0_f_byID.sql */
/* includes paid up accounts */
-- formatted twice: {} {}
-- waste the helpers.sixdigitdate x2 
-- & 2nd time with personID
SELECT slot_cost FROM Kayak_Slots
WHERE personID = {{}}
;
