/* no_email.sql */

SELECT P.personID, P.first, P.last, P.address, P.town, P.state,
                    P.postal_code
FROM People AS P

JOIN 
    Person_Status AS PS
ON P.personID = PS.personID

JOIN
    Stati as St
ON St.statusID = PS.statusID

WHERE St.key = 'm' AND P.email = ''

ORDER BY P.last, P.first
;

/* need to exclude those who are not members */
