#!/usr/bin/env python3

# File: tests/test_routines.py

import unittest
import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import routines
from code import club
from code import helpers
today = helpers.eightdigitdate

"""
Only a tiny fraction of the code is tested.
Suggested priority for writing test code:
    --
"""
class Test_keys_from_schema(unittest.TestCase):

    def test_default(self):
        keys = routines.keys_from_schema("People")
        self.assertEqual(keys, 
            routines.keys_from_schema("People",brackets=(0,0)))
        for begin,end in ((0,0), (1,0), (2,1), (0, 3),):
            ending = len(keys) - end
            self.assertEqual(keys[begin:ending], 
                routines.keys_from_schema("People",
                    brackets=(begin,end)))

class Test_keys_from_query(unittest.TestCase):

    def test_asterix(self):
        query = "SELECT * FROM People;"
        keys = routines.keys_from_query(query)
        self.assertEqual(keys, routines.keys_from_schema(
                                "People"))


class Test_get_demographic_dict(unittest.TestCase):

    def test_alex_kleider(self):
        d = routines.get_demographic_dict(97)
        self.assertTrue(d['first'] == 'Alex')
        self.assertEqual(d['last'], 'Kleider')


class Test_Assignations(unittest.TestCase):
        
    def test_assign_inductees4payment(self):
        """
        Testing code.club.assign_inductees4payment(holder)
        which requires Sql.inducted.sql
        """
        holder = club.Holder()
#       routines.assign_inductees4payment(holder)
#       self.assertEqual(holder.working_data, {})
#       for key, value in holder.working_data.items():
#           if type(value) == dict:
#               print(f"{key}:")
#               for k, v in value.items():
#                   print(f"    {k}: {v}")
#           else:
#               print(f"{key}: {value}")
        holder.delete_instance()
        
class Test_querykeys(unittest.TestCase):

    queries_and_keys = [
        ("""-- provides the applicant data
        SELECT P.personID, P.first, P.last, P.suffix,
            P.phone, P.address, P.town, P.state, P.postal_code,
            P.country, P.email,
            A.sponsor1ID, P1.first, P1.last,
            A.sponsor2ID, P2.first, P2.last,
            A.app_rcvd, A.fee_rcvd, 
            A.meeting1, A.meeting2, A.meeting3,
            A.approved, A.dues_paid
        FROM Applicants AS A
        JOIN People AS P
        ON P.personID = A.personID
        JOIN People AS P1
        ON P1.personID = A.sponsor1ID
        JOIN People AS P2
        ON P2.personID = A.sponsor2ID
        WHERE A.notified = ""
        ; """, 
         ("P_personID", "P_first", "P_last", "P_suffix",
            "P_phone", "P_address", "P_town", "P_state",
            "P_postal_code",
            "P_country", "P_email",
            "A_sponsor1ID", "P1_first", "P1_last",
            "A_sponsor2ID", "P2_first", "P2_last",
            "A_app_rcvd", "A_fee_rcvd", 
            "A_meeting1", "A_meeting2", "A_meeting3",
            "A_approved", "A_dues_paid",)),

        (f"""-- provides ordering and consistency ck
        SELECT P.personID, P.first, P.last, P.suffix,
            PS.statusID, S.text
        FROM People as P
        JOIN Person_Status as PS ON PS.personID = P.personID
        JOIN Stati as S on S.statusID = PS.statusID
        WHERE (PS.begin = "" or PS.begin <= {today})
            AND (PS.end = "" or PS.end > {today})
            AND PS.statusID < 11
        ORDER BY PS.statusID, P.last, P.first
        ;""",
         ("P_personID", "P_first", "P_last", "P_suffix",
            "PS_statusID", "S_text")),

        ("""
        SELECT * FROM People;
        """,
         ("personID", "first", "last", "suffix", "phone", "address",
          "town", "state", "postal_code", "country", "email")),


        ("SELECT * FROM People ORDER BY last LIMIT 3;",
         ("personID", "first", "last", "suffix", "phone", "address",
          "town", "state", "postal_code", "country", "email")),
         ]

    def test_querykeys(self):
        for query, keys in self.queries_and_keys:
            self.assertEqual(routines.query_keys(query),
                [key for key in keys])

if __name__ == '__main__':
    unittest.main()
