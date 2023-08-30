/* Sql/create_newApplicants_table.sql */
CREATE TABLE newApplicants(
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
    notified TEXT DEFAULT ''
--  UNIQUE(personID, app_rcvd)
    PRIMARY KEY(personID, app_rcvd)
                        );
/* Error generated:
sqlite> .read Sql/create_newApplicants_table.sql
Error: near line 2: near "(": syntax error
*/

