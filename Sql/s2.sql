/* Sql/s2.sql */

/* See docstring for code/ck_data.ck_appl_vs_status_tables() */

SELECT P.personID, P.first, P.last, P.suffix
FROM People       AS P
JOIN Person_Status AS PS
  ON PS.personID = P.personID
  WHERE PS.statusID = 5
    AND PS.end = ''
ORDER BY P.last, P.first, P.suffix
    ;
