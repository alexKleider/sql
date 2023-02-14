SELECT 
    People.first, People.last, People.phone,
    Stati.key
FROM
    People
INNER JOIN
    Person_Status
ON
    People.personID = Person_status.personID
INNER JOIN
    Stati
ON
    Stati.statusID = Person_Status.statusID
WHERE
    Stati.key IN ("a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
ORDER BY Stati.key
;


