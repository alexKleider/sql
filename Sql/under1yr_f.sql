/* under1yr_f.sql */
/* selects those who've been members < 1 yr. */
/* must be formated with (routines.sixdigitdate - 10000). */
SELECT P.first, P.last, S.text, PS.begin, PS.end from People as P
JOIN Person_Status as PS
ON P.personID = PS.personID
JOIN Stati as S
ON PS.statusID = S.statusID
WHERE S.statusID = 15
AND PS.begin > {};

