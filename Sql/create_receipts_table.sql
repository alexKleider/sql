/* Sql/create_receipts_table.sql */
CREATE TABLE Receipts (
    ReceiptID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    date_recieved TEXT NOT NULL,
    dues INTEGER DEFAULT NULL,
    dock INTEGER DEFAULT NULL,
    kayak INTEGER DEFAULT NULL,
    mooring INTEGER DEFAULT NULL,
    acknowledged TEXT DEFAULT NULL
                 --date value
    );
