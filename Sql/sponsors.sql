/* sponsors.sql */

/* retrieves sponsors of person who's ID is provided
in the formatting sequence */

SELECT
    P.first, P.last
FROM
    People as P
JOIN
    Sponsors as Sp
ON
    P.personID = Sp.sponsorID
WHERE
    Sp.personID = {}
;
    
    
