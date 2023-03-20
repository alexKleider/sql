/*  Sql/get_stati_keys_by_personID.sql */
/*  Requires a one tuple parameter (a personID) 
    retrieves that person's status key(s)(not statusID) */
SELECT St.key
FROM Stati AS St
JOIN Person_Status AS PS
ON PS.statusID = ST.statusID
WHERE PS.personID = ?
;
