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
JOIN
    Stati as St
ON
    St.statusID = PS.statusID
WHERE 
    St.statusID IN (11, 15)  -- New Member & Current Member
    AND (PS.end = '' OR PS.end > {})
-- must format date membership ended or will end.
-- use code.helpers.sixdigitdate
ORDER BY
    P.last, P.first
;
