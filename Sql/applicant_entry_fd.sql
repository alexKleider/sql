/* Sql/applicant_entry_fd.sql */
INSERT INTO Applicants (personID, 
        sponsor1ID, sponsor2ID,
        app_rcvd, fee_rcvd)
VALUES ({personID}, 
        {sponsor1ID},{sponsor2ID},
        {app_rcvd}, {fee_rcvd})
;
