/* Sql/applicants2.sql */
SELECT
    P.first, P.last, P.suffix,
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1, sponsor2,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, inducted, dues_paid
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
WHERE Ap.dues_paid = ''
ORDER BY P.last, P.first
;
