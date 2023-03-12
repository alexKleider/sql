/* Sql/ap_stati_in_use.sql */

SELECT P.personID, P.first, P.last, P.suffix, S.statusID, S.key
FROM People AS P
JOIN Person_Status AS PS
ON P.personID = PS.personID
JOIN Stati AS S
ON PS.statusID = S.statusID
WHERE S.key LIKE  'a%'
ORDER BY S.key
;

/*
results of above query (as of
Sat 11 Mar 2023 12:01:05 PM PST):

sqlite> .read Sql/stati_contents.sql
2|a|Application complete but not yet acknowledged
1|a-|Application received without fee
3|a0|Applicant (no meetings yet)
4|a1|Attended one meeting
5|a2|Attended two meetings
6|a3|Attended three (or more) meetings
8|ad|Inducted & notified, membership pending payment of dues
7|ai|Inducted, needs to be notified
11|am|New Member
9|av|Vacancy ready to be filled pending payment of dues
10|aw|Inducted & notified, awaiting vacancy
13|ba|Postal address => mail returned
12|be|Email on record being rejected
14|h|Honorary Member
16|i|Inactive (continuing to receive minutes)
15|m|Member in good standing
17|r|Retiring/Giving up Club Membership
18|t|Membership terminated (probably non payment of fees)
19|w|Fees being waived
20|z1_pres|President
21|z2_vp|VicePresident
22|z3_sec|Secretary of the Club
23|z4_treasurer|Treasurer
24|z5_d_odd|Director- term ends Feb next odd year
25|z6_d_even|Director- term ends Feb next even year
26|zae|Application expired or withdrawn
27|zzz|No longer a member
*/

