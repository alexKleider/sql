/* applicants.sql */

        SELECT
            St.statusID, St.key, P.personID,
            P.first, P.last
        FROM People AS P
        JOIN Person_Status AS PS
            ON PS.personID = P.personID
        JOIN Stati AS St
            ON St.statusID = PS.statusID
        WHERE
            St.key IN ("a-", "a" , "a0", "a1", "a2",
                "a3", "ai", "ad", "av", "aw", "am")
        ORDER BY St.key
    ;
