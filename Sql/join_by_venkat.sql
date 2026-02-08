
/* File: join_by_venkat.sql */
/* Must 'insert' today's date.

        SELECT app.personID, app.first, app.last,
                  sp1.first, sp1.last,
                  sp2.first, sp2.last 
        FROM Applicants AS appln,
             People AS app,
             People AS sp1,
             People AS sp2,

            Person_Status as PS

        WHERE appln.personID = app.personID
        AND   appln.sponsor1ID = sp1.personID
        AND   appln.sponsor2ID = sp2.personID
        AND appln.notified = ''      -- this line accomplished 
                                -- what the JOIN below was trying
                                -- to do....
        
        AND (PS.personID = app.personID
            AND PS.statusID in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
            AND PS.begin <= "{}"
            AND (PS.end >= "{}" OR PS.end = ""))

/*        JOIN Person_Status AS PS
        ON (PS.personID = app.personID
            AND PS.statusID in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
            AND PS.begin <= "{}"
            AND (PS.end >= "{}" OR PS.end = ""))
 */           
        ;
