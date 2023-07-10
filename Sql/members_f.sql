/* Sql/members_f.sql */
-- !! Requires formatting !!
--    ..but only once!
-- retrieves member demographics
SELECT
    P.personID, P.first, P.last, P.suffix, P.email, P.address,
    P.town, P.state, P.postal_code, P.country 
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
AND (PS.end = '') OR PS.end > {}
-- must format: use code.helpers.sixdigitdate
ORDER BY
    P.last, P.first, P.suffix
;
