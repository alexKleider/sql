/* Sql/list4join_ff.sql */
-- !! Requires formatting !!  (eightdigitdate x2)
-- retrieves member demographics _with_ trailing statusID
-- includes retiring, inactive & honorary members (if any.)
-- personID is last item
SELECT
    first, last, suffix, phone, address,
    town, state, postal_code, email,
    PS.statusID, PS.begin
--   ^ [9]         ^ [10]
--    St.key, P.first, P.last
    , P.personID  -- [-1]
--  added personID which may ==> a bug!!
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE(
    PS.statusID IN (11, 14, 15, 16, 17)
            -- New, honorary, current, inactive & retiring
    AND ((PS.begin = '') OR (PS.begin <= {}))   -- today
    AND((PS.end = '') OR (PS.end > {}))   -- today
    )
-- must format comparison date membership ended or will end.
-- use code.helpers.eightdigitdate x 2
ORDER BY
    P.last, P.first, p.suffix
;

