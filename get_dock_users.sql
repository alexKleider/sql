-- get_dock_users.sql

SELECT 
    People.first, People.last,
    Dock_Privileges.cost
FROM
   People
INNER JOIN
   Dock_Privileges
ON
    Dock_Privileges.personID = People.personID 
ORDER BY
    People.last, People.first
;


