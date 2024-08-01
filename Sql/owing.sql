/*
   File: owing.sql

   LEFT JOIN and LEFT OUTER JOIN are synonyms
   see Notes/commands
     https://www.sqlservertutorial.org/sql-server-joins/
*/

SELECT P.personID, P.last, P.first, P.suffix,
        D.dues_owed, DP.cost, KS.slot_cost, M.owing
        FROM People AS P
        LEFT JOIN Dues AS D ON D.personID = P.personID
        LEFT JOIN Moorings AS M ON P.personID = M.personID
        LEFT JOIN Kayak_Slots AS KS ON KS.personID = P.personID
        LEFT JOIN Dock_Privileges AS DP ON DP.personID = P.personID
        WHERE (D.dues_owed > 0
            or DP.cost > 0 
            or KS.slot_cost > 0 
            or M.owing > 0 )
        ORDER BY P.last;

