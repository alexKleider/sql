/* Sql/mooring_f_byID.sql */
SELECT M.owing
FROM Moorings as M
JOIN Person_Status as PS
ON M.personID =PS.personID
WHERE PS.statusID IN (11, 15)
AND PS.end < {}
AND M.personID = {{}}
AND D.dues_owed > 0
;
