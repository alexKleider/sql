/* Sql/owing_by_ID.sql */
-- requires a one tuple: (personID, )
SELECT P.first, P.last, P.suffix, P.email,
        P.address, P.town, P.state, P.postal_code, P.country,
        D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
WHERE P.personID = ?;
