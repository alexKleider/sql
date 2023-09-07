/* Sql/members1stYr_f.sql */
/* "members in their first year of membership" */

SELECT
    P.personID, P.first, P.last, P.suffix, P.email, P.address,
    P.town, P.state, P.postal_code, P.country 
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE (
    PS.statusID = 11
    AND (PS.begin <= {})   -- today
    AND((PS.end = '') OR (PS.end > {}))   -- today
    )
-- must format: use code.helpers.eightdigitdate
ORDER BY
    P.last, P.first, P.suffix
;
