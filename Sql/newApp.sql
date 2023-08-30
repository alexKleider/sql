/* File: Sql/newApp.sql */
/* Gives a syntax error!
   Being kept only for reference should the reason
   for the syntax error ever be discovered.
*/
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;
ALTER TABLE Applicants RENAME TO oldApplicants;
CREATE TABLE Applicants (
    personID INTEGER NOT NULL,
    sponsor1ID INTEGER NOT NULL,
    sponsor2ID INTEGER NOT NULL,
    app_rcvd TEXT NOT NULL,
    fee_rcvd TEXT DEFAULT '',
    meeting1 TEXT DEFAULT '',
    meeting2 TEXT DEFAULT '',
    meeting3 TEXT DEFAULT '',
    approved TEXT DEFAULT '',
    dues_paid TEXT DEFAULT '',
    notified TEXT DEFAULT '',
    PRIMARY KEY(personID, app_rcvd)
                        );
INSERT INTO Applicants
SELECT * FROM oldApplicants;
DROP TABLE oldApplicants;
COMMIT;
PRAGMA foreign_keys=on;
