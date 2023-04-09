/* Sql/set_date.sql */
UPDATE Applicants
SET meeting VALUES :meeting
WHERE personID = :personID
;
/* {'meeting': '230303',
    'personID': pIDA, } */
