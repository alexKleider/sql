-- File: Sql/receipts_f.sql --

SELECT P.personID, P.last, P.first, P.suffix,
    R.date_received, R.ap_fee, R.dues, R.dock, R.kayak, R.mooring
FROM People as P
JOIN Receipts as R
    on P.personID = R.personID
WHERE R.date_received > "{}"
ORDER by R.date_received, P.last, P.first, P.suffix
;

