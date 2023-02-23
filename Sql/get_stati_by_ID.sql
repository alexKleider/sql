/* Sql/get_stati_by_ID */

/* One format slot for a personID */

SELECT
    St.key
FROM 
    Stati AS St
JOIN
    Person_Status AS PS
ON
    PS.statusID = ST.statusID
WHERE
    PS.personID = {};

