/* Sql/get_dock_users.sql */
/* in theory- could return an empty list */
/* will probably be redacted in favour of Sql/dock.sql */
SELECT P.first, P.last, D.cost
FROM
   People AS P
INNER JOIN
   Dock_Privileges AS D
ON
    D.personID = P.personID 
ORDER BY
    P.last, P.first
;
