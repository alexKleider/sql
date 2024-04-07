/* Sql/mem4join_ff.sql */
-- !! Requires formatting !!  (eightdigitdate x2)
-- retrieves member demographics _with_ trailing statusID
-- to distinguish 'member in good standing' vs 1st year.
-- results in 100 members
-- personID is last item
SELECT
    first, last, suffix, phone, address,
    town, state, postal_code, email,
    PS.statusID, PS.begin
--   ^ [9]         ^ [10]
--    St.key, P.first, P.last
    , P.personID
--  added personID which may ==> a bug!!
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE( 
    PS.statusID IN (11, 15)  -- New & Current Member
    AND ((PS.begin = '') OR (PS.begin <= {}))   -- today
    AND((PS.end = '') OR (PS.end > {}))   -- today
    )
-- must format comparison date membership ended or will end.
-- use code.helpers.eightdigitdate x 2
ORDER BY
    P.last, P.first, p.suffix
;

