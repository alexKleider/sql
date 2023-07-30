/* Sql/getApplicants.sql */
/* collects _current_ applicants */
SELECT
    P.personID,
    P.first, P.last, P.suffix,  -- 1:4           6
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,       -- -10
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, dues_paid, notified
FROM Applicants AS Ap
JOIN 
    People AS P
ON Ap.personID = P.personID
WHERE 
    Ap.dues_paid = ''  --exclude those already made members
AND NOT 
    Ap.notified = 'dropped'
;
