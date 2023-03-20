/*  Sql/get_stati_row_by_personID.sql */
/*  Requires a one tuple parameter (a personID) 
    retrieves that person's stati (ID, key, text) */
SELECT St.statusID, St.key, St.text
FROM Stati AS St
JOIN Person_Status AS PS
ON PS.statusID = ST.statusID
WHERE PS.personID = ?
;
