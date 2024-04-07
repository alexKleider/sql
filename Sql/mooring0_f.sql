/* Sql/mooring0_f.sql */
-- {} {}  to 'use up' eightdigitdate
SELECT personID, owing
FROM Moorings
WHERE personID = {{}}
AND not personID = null
;
