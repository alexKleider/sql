/* Sql/applicants.sql */
SELECT
    St.key, P.first, P.last, 
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID,
    app_rcvd, fee_rcvd, meeting1, meeting2, meeting3,
    approved, inducted, dues_paid, St.text
FROM Applicants AS Ap
JOIN People AS P
ON Ap.personID = P.personID
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati as St
ON St.statusID = PS.statusID
WHERE St.key IN ("a-", "a" , "a0", "a1", "a2",
        "a3", "ai", "ad", "av", "aw", "am")
ORDER BY St.key
;
