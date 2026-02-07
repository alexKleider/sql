
/* applicants_current.sql */
/* based on Applicant table */

SELECT 
    P.personID, St.key, P.first, P.last, 
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, dues_paid, St.text
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID


