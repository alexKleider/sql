/* Sql/dock_f_byID.sql */
/* includes paid up accounts */
-- must be formatted twice:
-- once with helpers.sixdigitdate
-- & 2nd time with personID
SELECT D.cost
FROM Dock_Privileges as D
JOIN Person_Status as PS
ON D.personID = PS.personID
WHERE PS.statusID IN (11, 15) 
AND PS.end < {}
AND D.personID = {{}}
AND D.dues_owed > 0
;
