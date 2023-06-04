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
    St.key = 'm'
    AND (PS.end = '' OR PS.end > {})
ORDER BY
    P.last, P.first
;
