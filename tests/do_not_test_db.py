#!/usr/bin/env python3

# File: do_not_test_db.py

import unittest
import os
import shutil
from code import club

class TestDataEntry(unittest.TestCase):

    def setUp(self):
        """copy data to temp file"""
        shutil.copy2(club.db_file_name, club.bu_while_testing)
        print(
        f"Copying {club.db_file_name} to {club.bu_while_testing}")

    def test_files_are_the_same(self):
        with open(club.db_file_name, 'rb') as inf_original:
            original = inf_original.read()
        print(f"Opened and read {inf_original.name}")
        with open(club.bu_while_testing, 'rb') as inf_copy:
            copy = inf_copy.read()
        print(f"Opened and read {inf_copy.name}")
        self.assertEqual(original, copy)

    def tearDown(self):
        """restore data from, then destroy, temp file"""
        shutil.copy2(club.bu_while_testing,club.db_file_name)
        print(
        f"Copied {club.bu_while_testing} to {club.db_file_name}")
        os.remove(club.bu_while_testing)
        print(
        f"Deleted temporary holding file {club.bu_while_testing}")


if __name__ == "__main__":
    unittest.main()

