/* Sql/ad.sql */

/* See docstring for code/ck_data.ck_appl_vs_status_tables() */
/* Selects those having statusID 7:
                Inducted but yet to be notified */

SELECT P.personID, P.first, P.last, P.suffix
FROM People     AS P
JOIN Applicants  AS A
ON A.personID = P.personID
WHERE A.approved != ""
  AND A.dues_paid = ""
  AND A.notified = ""
ORDER BY P.last, P.first, P.suffix
;
