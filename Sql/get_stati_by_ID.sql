/*  Sql/get_stati_by_ID */
/*  One format slot for a personID */
/*  retrieves the status key (not ID) (possibly more than one)
    for the person who's ID is provided as a one tuple
    Not yet used!
*/
SELECT St.key
FROM Stati AS St
JOIN Person_Status AS PS
ON PS.statusID = ST.statusID
WHERE PS.personID = ?;

