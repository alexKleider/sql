/* File: Sql/mooring-csv.sql */

/* Used to create a csv file. */
-- Headers are:
-- personID, first, last, code, cost, owing

SELECT P.personID, P.first, P.last, M.mooring_code, M.mooring_cost, M.owing from People as P join Moorings as M where P.personID = M.personID order by M.mooringID;
