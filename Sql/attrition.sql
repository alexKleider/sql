/* Sql/attrition.sql */
SELECT P.first, P.last, P.suffix, A.date, A.reason
FROM People as P
JOIN Attrition as A
WHERE P.personID = A.personID;
