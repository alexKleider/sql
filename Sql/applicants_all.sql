/* Sql/applicants_all.sql */
SELECT
    P.personID, P.first, P.last, P.suffix,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, dues_paid, notified
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
-- ORDER BY P.last, P.first
ORDER BY app_rcvd, P.last, P.first
;
