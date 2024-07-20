/* File: Sql/statements.sql
similar to Sql/owing.sql but more demographics
Note that this is used for a revised method of sending bills.
The previous method collected all members first and then checked
what was owing by each.
This method picks out only those who owe money. (Membership is
not checked!)
*/
SELECT P.personID, P.last, P.first, P.suffix,
        P.email, P.address, P.town, P.state,
        P.postal_code, P.country,
        D.dues_owed, DP.cost, KS.slot_cost, M.owing
        FROM People AS P
        LEFT JOIN Dues AS D ON D.personID = P.personID
        LEFT JOIN Moorings AS M ON P.personID = M.personID
        LEFT JOIN Kayak_Slots AS KS ON KS.personID = P.personID
        LEFT JOIN Dock_Privileges AS DP ON DP.personID = P.personID
        WHERE (D.dues_owed>0 or DP.cost > 0 or M.owing > 0 )
        ORDER BY P.last;

