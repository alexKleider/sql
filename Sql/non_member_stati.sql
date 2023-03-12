/* Sql/non_member_stati.sql */
    SELECT P.personID, P.first, P.last, P.suffix, S.key
    FROM People AS P
    JOIN Person_Status as PS
    JOIN Stati AS S
    WHERE P.personID = PS.personID
    AND PS.statusID = S.statusID
    AND NOT S.key = 'm'  -- exclusive of members
        -- otherwise result is too long!
        -- NOTE: includes members with stati other than 'm'.
    ORDER BY P.personID
    ; 
