
/* File: Sql/oldtimersFF.sql */

/* Provides an ordered listing of when current
   members joined ordered by longest first.  */

-- requires fomatting: a date 1yr later than current date
-- and set LIMIT on how many you want to be listed

SELECT P.first, P.last, S.begin 
FROM People as P
JOIN Person_Status as S
WHERE S.begin != '' AND (S.end >"{}" OR end = "")
AND P.personID = S.personID
ORDER BY S.begin
LIMIT {};
