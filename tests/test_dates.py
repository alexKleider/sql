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


class Test_file_acknowledgement(unittest.TestCase):

    def setUp(self):
        self.ret = []
        holder = club.Holder()
        shutil.copyfile(holder.db_file_name, club.temp_db)
        holder.db_file_name = club.temp_db
        holder.which = content.content_types["thank"]
        holder.direct2json_file = True
        self.ret.extend(commands.assign_templates(holder))
        data_listing = [
          dict(
            personID=97,
            first='Alex',
            last='Kleider',
            suffix='',
            address='PO Box 277',
            town='Bolinas',
            state='CA',
            postal_code='94924',
            country='USA',
            email='alex@kleider.ca',
            dues=200,
            total=200,
            payment=200,
            ),
          dict(
            personID=144,
            first='Don',
            suffix='',
            last='Murch',
            address='140 Olema-Bolinas Rd',
            town='Bolinas',
            state='CA',
            postal_code='94924',
            country='USA',
            email='dwmurch@gmail.com',
            dues=200,
            mooring=152,
            total=352,
            payment=352,
            )
          ]

        for data in data_listing:
            self.ret.extend(dates.file_acknowledgement(holder, data))
        with open(check_file, 'w') as outf:
            outf.write('\n'.join(self.ret))
        print(f"Check file '{check_file}'")
    
    def tearDown(self):
        pass

    def test_alex_kleider(self):
        d = dates.get_demographic_dict(97)
        self.assertTrue(d['first'] == 'Alex')
        self.assertEqual(d['last'], 'Kleider')


if __name__ == '__main__':
    unittest.main()

