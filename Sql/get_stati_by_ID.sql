/*  Sql/get_stati_by_ID */
/*  Requires a one tuple parameter (a personID) 
    retrieves that person's status key(s)(not statusID)
    Not yet used!  */
SELECT St.key
FROM Stati AS St
JOIN Person_Status AS PS
ON PS.statusID = ST.statusID
WHERE PS.personID = ?
;
