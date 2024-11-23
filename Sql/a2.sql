/* Sql/a2.sql */

/* See docstring for code/ck_data.ck_appl_vs_status_tables() */
SELECT P.personID, P.first, P.last, P.suffix
FROM People     AS P
JOIN Applicants  AS A
ON A.personID = P.personID
WHERE A.notified = ""
  AND A.meeting1 != ""
  AND A.meeting2 != ""
  AND A.meeting3 = ""
  AND A.notified = ""
ORDER BY P.last, P.first, P.suffix
;
