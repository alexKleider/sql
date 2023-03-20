/* Sql/show_applicant_data4ID.sql */
SELECT P.first, P.last, P.suffix,
    A.sponsor1, A.sponsor2, A.app_rcvd, A.fee_rcvd,
    A.meeting1, A.meeting2, A.meeting3,
    A.approved, A.inducted, A.dues_paid
FROM Applicants as A
JOIN People as P
ON P.personID = A.personID
WHERE P.personID = ?
;
