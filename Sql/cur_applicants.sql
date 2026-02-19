/*  File: Sql/cur_applicants.sql
cur_applicants_query as defined in code/applicant_update.py
*/
    SELECT P.personID, P.first, P.last, P.email,
        A.sponsor1ID, S1.first, S1.last, S1.email,
        A.sponsor2ID, S2.first, S2.last, S2.email,
        A.app_rcvd, A.fee_rcvd,
        A.meeting1, A.meeting2, A.meeting3,
        A.approved, A.dues_paid, A.notified
    FROM people as P,
        Applicants as A,
        people as S1,
        people as S2
    WHERE P.personID = A.personID
    AND A.sponsor1ID = S1.personID
    AND A.sponsor2ID = S2.personID
    AND A.notified = ""
    ;
