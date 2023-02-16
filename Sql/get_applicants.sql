/* get_applicants.sql */

SELECT 
    P.first, P.last, P.phone,
    St.text
FROM
    People AS P
INNER JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
INNER JOIN
    Stati AS St
ON
    St.statusID = PS.statusID
WHERE
    St.key IN ("a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
ORDER BY St.key
;


