/* applicants.sql */
        SELECT
            Stati.key,
            People.first, People.last
        FROM People
        JOIN Person_Status
            ON Person_Status.personID = People.personID
        JOIN Stati
            ON Stati.statusID = Person_Status.statusID
        WHERE
            Stati.key IN ("a-", "a" , "a0", "a1", "a2",
                "a3", "ai", "ad", "av", "aw", "am")
        ORDER BY Stati.key
    ;
