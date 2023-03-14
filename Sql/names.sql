/* Sql/names.sql */
SELECT
    first, last
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
JOIN
    Stati as St
ON
    St.statusID = PS.statusID
WHERE 
    St.key IN ("m", "a-", "a" , "a0", "a1", "a2",
            "a3", "ai", "ad", "av", "aw", "am")
ORDER BY
    P.last, P.first
;
