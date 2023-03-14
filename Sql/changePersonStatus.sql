/* Sql/changePersonStatus.sql */
-- requires a 3 tuple param:
        -- new status ID
        -- existing personID
        -- existing statusID to be replaced.
UPDATE Person_Status
SET statusID = ?
WHERE personID = ?
AND statusID = ?
;
