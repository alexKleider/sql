/* Sql/app4join_ff.sql */
-- used by code/show.py: query_files
-- JOINs People, Stati, Person_Status, Applicants
-- !! Requires formatting !!  (eightdigitdate x2)
-- retrieves applicant demographics _with_ trailing
-- personID, statusID & status text

SELECT
    first, last, suffix, phone, address,  -- 0..4
    town, state, postal_code, email,      -- 5..8
    A.sponsor1ID, A.sponsor2ID,           -- 9, 10
    meeting1, meeting2, meeting3,         -- -6, -5, -4
    P.personID, S.statusID, S.text       -- -3, -2, -1
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
JOIN 
    Stati as S
ON 
    PS.statusID = S.statusID
JOIN
    Applicants as A
ON 
    P.personID = A.personID
WHERE( 
    PS.statusID < 11  -- all applicants
    AND ((PS.begin <= {}) OR (PS.begin = ''))   -- today
    AND((PS.end = '') OR (PS.end > {}))   -- today
    )
-- must format comparison date status ended or will end.
-- use code.helpers.eightdigitdate x 2
ORDER BY
    S.statusID, P.last, P.first, p.suffix
;
