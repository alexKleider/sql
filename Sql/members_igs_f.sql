/* Sql/members_igs_f.sql */
/* "members in good standing"  */

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
    PS.statusID = 15
    AND (PS.begin <= {})  -- today
    AND((PS.end = '') OR (PS.end > {}))  -- today
    )
-- must format: use code.helpers.eightdigitdate
ORDER BY
    P.last, P.first, P.suffix
;
