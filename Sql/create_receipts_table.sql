/* Sql/create_receipts_table.sql */
CREATE TABLE Receipts (
    ReceiptID INTEGER PRIMARY KEY,
    personID INTEGER NOT NULL,
    date_received TEXT NOT NULL,
    dues INTEGER DEFAULT 0,
    dock INTEGER DEFAULT 0,
    kayak INTEGER DEFAULT 0,
    mooring INTEGER DEFAULT 0,
    acknowledged TEXT DEFAULT 0
                 --date value
    );
