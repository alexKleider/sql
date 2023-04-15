/* Secret/update_meeting.sql */
/*
SELECT P.personID, P.first, P.last, P.suffix, A.sponsor1, app_rcvd, fee_rcvd, meeting1
FROM people AS P
JOIN Applicants AS A
ON P.personID = A.personID
AND P.last = '{}';

SELECT meeting3 FROM Applicants
WHERE personID = {};
*/
UPDATE Applicants
SET meeting1 = '230303'
WHERE personID = 29;

