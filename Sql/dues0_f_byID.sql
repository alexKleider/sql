/* Sql/dues0_f_byID.sql */
/* includes paid up accounts */
-- must be formatted twice:
-- once with helpers.sixdigitdate
-- & 2nd time with personID
SELECT D.dues_owed
FROM Dues as D
JOIN Person_Status as PS
ON D.personID = PS.personID
WHERE PS.statusID in (8, 11, 15)
AND (PS.end = '' OR PS.end > {})
AND (PS.begin = '' OR PS.begin < {})
AND D.personID = {{}}
;
