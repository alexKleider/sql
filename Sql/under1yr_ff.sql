/* under1yr_ff.sql */
/* selects those who've been members < 1 yr. */
/* must be formated with (routines.eightdigitdate - 10000). */
/* keys are: personID, first, last, suffix, text, begin, end */
SELECT 
    P.personID, P.first, P.last, P.suffix,
    S.text, PS.begin, PS.end 
FROM People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON PS.statusID = S.statusID
WHERE 
    (PS.statusID = 15
    AND NOT PS.begin < '{}'
    AND (PS.end = '' OR PS.end > '{}'))
OR
    (PS.statusID = 11
        AND NOT PS.begin < '{}' )
;
