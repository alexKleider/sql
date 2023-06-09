/* Sql/names_f.sql */
SELECT first, last
FROM People AS P
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati as St
ON St.statusID = PS.statusID
WHERE 
St.key IN ("m", "a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
AND (PS.end = 0 OR PS.end < {})
-- must insert today's date ^^ (helpers.todaysdate)
ORDER BY P.last, P.first
;
