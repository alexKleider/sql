/* Sql/applicants2.sql */
SELECT
    P.personID, P.first, P.last, P.suffix, P.phone,
    P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, dues_paid, notified
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
WHERE
    Ap.notified = ''
AND
    NOT Ap.notified LIKE "drop%"
ORDER BY P.last, P.first
;
