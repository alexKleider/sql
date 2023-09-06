 /* Sql/officers.sql */
 select P.personID, P.first, P.last, P.email, S.begin, S.statusID, S.end from People as P
   JOIN Person_Status as S
   on P.personID = S.personID
   where S.begin = ""
    and NOT S.statusID = 15
    ;

