/* Sql/a0-.sql */
-- application without fee
/* See docstring for code/ck_data.ck_appl_vs_status_tables() */
SELECT P.personID, P.first, P.last, P.suffix
FROM People     AS P
JOIN Applicants  AS A
ON A.personID = P.personID
WHERE A.fee_rcvd = ""
  AND A.notified = ''
ORDER BY P.last, P.first, P.suffix
;
