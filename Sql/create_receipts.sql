/* Sql/create_receipts.sql */
CREATE TABLE Receipts (
    ReceiptID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    dues INTEGER DEFAULT NULL,
    dock INTEGER DEFAULT NULL,
    kayak INTEGER DEFAULT NULL,
    mooring INTEGER DEFAULT NULL,
    acknowledged TEXT NOT NULL  --date value
    );
