/* Sql/show_f.sql */
-- !! Requires formatting !!
-- retrieves member demographics
SELECT
    first, last, suffix, phone, address,
    town, state, postal_code, email
--    St.key, P.first, P.last
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE( 
    PS.statusID IN (11, 15)  -- New & Current Member
    AND (PS.begin <= {})   -- today
    AND((PS.end = '') OR (PS.end > {}))   -- today
    )
-- must format date membership ended or will end.
-- use code.helpers.eightdigitdate x 2
ORDER BY
    P.last, P.first, p.suffix
;
