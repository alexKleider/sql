/* Sql/new_applicants_f.sql */
SELECT
    P.personID, P.last, P.first, P.suffix,
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID, PS.begin, PS.end
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
JOIN Person_Status as PS
ON Ap.personID = PS.personID
WHERE PS.statusID = 2
AND (PS.end = "" OR PS.end > {})
ORDER BY P.last, P.first, P.suffix
;
/* returns:
personID, last, first, suffix, phone, address, town, state,
postal_code, email, sponsor1, sponsor2, personID, begin, end
*/

