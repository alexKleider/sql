/* Sql/s3.sql */

/* See docstring for code/ck_data.ck_appl_vs_status_tables() */

SELECT P.personID, P.first, P.last, P.suffix
FROM People       AS P
JOIN Person_Status AS PS
  ON PS.personID = P.personID
  WHERE PS.statusID = 6
    AND PS.end = ''
ORDER BY P.last, P.first, P.suffix
    ;
