/* Sql/appIDs_owing.sql /*
SELECT personID FROM Applicants
WHERE approved != ''
AND dues_paid = ''
AND notified = ''
;
