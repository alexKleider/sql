/* 
File: Sql/venkat.sql

Compare with newbyquery found in code/show.py:
-it has explicit JOIN statements, this one does not.

query = """

*/
        SELECT app.first, app.last,
                  sp1.first, sp1.last,
                  sp2.first, sp2.last 
        FROM Applicants AS appln,
             People AS app,
             People AS sp1,
             People AS sp2
        WHERE appln.personID = app.personID
        AND   appln.sponsor1ID = sp1.personID
        AND   appln.sponsor2ID = sp2.personID
        ;
--      """

