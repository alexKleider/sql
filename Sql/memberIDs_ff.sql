/* Sql/memberIDs_ff.sql */
-- !! Requires formatting !! (x2!!)
-- Only one client found: code/commands.py still_owing_cmd()
-- retrieves personID for each member 
-- AND any inductees who haven't yet paid their dues.
-- Should NOT RESULTS IN DUPLICATES!!!! assuming
-- the Person_Status file is properly maintained...
-- i.e. no-one can have duplicate current status 8, 11 or 15!

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
AND (PS.begin <= {})
-- must format: use code.helpers.eightdigitdate
ORDER BY
    P.last, P.first, P.suffix
;
