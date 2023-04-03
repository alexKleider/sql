/* Sql/dues.sql */
/* wording on query to collect dues & fees outstanding */
SELECT P.personID, P.first, P.last, P.suffix, P.email,
        P.address, P.town, P.state, P.postal_code,
        D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
WHERE NOT D.dues_owed = 0;
