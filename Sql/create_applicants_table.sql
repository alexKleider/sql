/* Sql/create_applicants_table.sql */
CREATE TABLE Applicants (
    applicantID INTEGER PRIMARY KEY,
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
    );
