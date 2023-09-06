/* Sql/applicants1.sql */
/* Should be redacted: has an entry for each status
   passed through by the applicant!  i.e. diplicates!!
*/
SELECT
    St.key, P.personID, P.first, P.last, 
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, dues_paid, St.text
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati as St
ON St.statusID = PS.statusID
WHERE Ap.notified = ''
ORDER BY St.key, P.last, P.first, P.suffix
;
