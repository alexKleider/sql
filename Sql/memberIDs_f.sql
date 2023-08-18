/* Sql/memberIDs_f.sql */
-- !! Requires formatting !!
--    ..but only once!
-- retrieves personID for each member 
-- AND inductees who haven't yet paid their dues.
SELECT
    P.personID, P.first, P.last, P.suffix
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
JOIN
    Stati as St
ON
    St.statusID = PS.statusID
WHERE St.statusID in (8, 11, 15)
AND ((PS.end = '') or (PS.end > {}))
-- must format: use code.helpers.eightdigitdate
ORDER BY
    P.last, P.first, P.suffix
;
