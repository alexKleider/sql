/* Sql/members_f.sql */
-- !! Requires formatting: eightdigitdate x2!!
SELECT
    P.personID, P.first, P.last, P.suffix, P.email, P.address,
    P.town, P.state, P.postal_code, P.country 
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE
(PS.statusID in (11, 15))
AND (PS.begin = '' OR PS.begin <= {})
AND (PS.end = '' OR PS.end > {})
ORDER BY
    P.last, P.first, P.suffix
;

