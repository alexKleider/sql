/* get_dock_users.sql */

SELECT 
    P.first, P.last,
    D.cost
FROM
   People AS P
INNER JOIN
   Dock_Privileges AS D
ON
    D.personID = P.personID 
ORDER BY
    P.last, P.first
;


