/* Sql/memIDs_f.sql */
-- better alternative to Sql/memberIDs_f.sql
-- no duplicates and _only_ members
-- inductees who haven't paid dues are _not_included
SELECT
    P.personID, P.first, P.last, P.suffix, PS.begin
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
WHERE St.statusID in (11, 15)
AND ((PS.end = '') or (PS.end > {}))
AND (PS.begin <= {})
ORDER BY P.personID
;
