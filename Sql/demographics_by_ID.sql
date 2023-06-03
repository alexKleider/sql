/* Sql/demographics_by_ID.sql */
-- needs an ID inserted
SELECT  first, last, suffix, address, town,
        state, postal_code, country, email
FROM People as P
WHERE P.personID = ?;
