/* Sql/dues_et_demographics_by_ID.sql */
-- needs an ID inserted
SELECT  P.first, P.last, P.suffix,
        P.address, P.town, P.state, P.postal_code, P.country,
        P.email,
        D.dues_owed
FROM People as P
JOIN Dues as D
ON P.personID = D.personID
WHERE P.personID = ?;
