/* Sql/applicants_from_stati.sql */
SELECT P.personID, P.last, P.first, P.suffix, S.key, S.text
FROM Stati as S
JOIN Person_Status as PS      ON S.statusID = PS.statusID
JOIN People as P              ON P.personID = PS.personID
WHERE PS.end = ''
    AND S.key  IN ("a-", "a" , "a0", "a1", "a2",
                  "a3", "ai", "ad", "av", "aw")
-- ORDER BY S.statusID, P.last, P.first
ORDER BY P.last, P.first
;
