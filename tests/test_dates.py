#!/usr/bin/env python3

# File: tests/test_dates.py

import unittest
import sys
import os
sys.path.insert(0, os.path.split(sys.path[0])[0])
import shutil
from code import dates
from code import club
from code import commands
from code import content

temp_db = club.temp_db
check_file = '2check.txt'

class Test_get_demographic_dict(unittest.TestCase):

    def test_alex_kleider(self):
        d = dates.get_demographic_dict(97)
        self.assertTrue(d['first'] == 'Alex')
        self.assertEqual(d['last'], 'Kleider')

problem = """
class TestInstanceDeletion(unittest.TestCase):
    def setUp(self):
        self.holder = club.Holder()

    def test1(self):
        self.holder.attr = "attr1"
        self.assertEqual(self.holder.attr, "attr1")

    def test2(self):
        self.holder.attr = "attr2"
        self.assertEqual(self.holder.attr, "attr2")


    def tearDown(self):
        self.holder.delete_instance()
#       print("deleted an Holder instance")
"""

if __name__ == '__main__':
    unittest.main()

