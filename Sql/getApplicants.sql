/* Sql/getApplicants.sql */
/* collects _current_ applicants */
SELECT
    P.personID,
    P.first, P.last, P.suffix,  -- 1:4           6
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1, sponsor2,       -- -10
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, inducted, dues_paid
FROM Applicants AS Ap
JOIN 
    People AS P
ON Ap.personID = P.personID
WHERE
    Ap.dues_paid = ''  --exclude those already made members
OR  Ap.dues_paid = 'zae'  -- and those who have dropped out
;
