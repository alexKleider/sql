#!/usr/bin/env python3

# File: tests/test_routines.py

import unittest
import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
from code import routines
from code import club

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
        

if __name__ == '__main__':
    unittest.main()
