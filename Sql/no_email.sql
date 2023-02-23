/* no_email.sql */

SELECT personID, first, last, address, town, state, postal_code
FROM People
WHERE email = ''; 

