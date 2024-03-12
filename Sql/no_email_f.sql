/* no_email_f.sql */
SELECT P.personID, P.first, P.last, P.address, P.town, P.state,
                    P.postal_code
FROM People AS P
JOIN 
    Person_Status AS PS
ON P.personID = PS.personID
JOIN
    Stati as St
ON St.statusID = PS.statusID
WHERE P.email = ''
    AND St.key IN ('m', 'am', 'h', 'i', 'r')
    AND ((PS.end = "") OR (PS.end > {})) 
ORDER BY P.last, P.first
;
