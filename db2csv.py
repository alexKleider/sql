#!/usr/bin/env python3

# File: db2csv.py

"""
Backs up the data base (Secret/club.db) by creating a csv file
for each table, putting them all into a separate directory,
and then creating a zip file to be backed up on Google Drive.
"""

import os
import csv
import shutil
from code import club
from code import helpers
from code import routines

tempdir = "TempZIP_Dir"
zip_name = f"{helpers.eightdigitdate4filename}_db_bu_as_CSVs"
tables = routines.fetch(
        """SELECT name FROM sqlite_master
           WHERE type='table';""", from_file=False)
tables = [table[0] for table in tables]
os.mkdir(tempdir)
for table in tables:
    file_name = tempdir +'/' + f"{table}.csv"
    keys = routines.keys_from_schema(table)
    with open(file_name, 'w', newline='') as stream:
        csv_writer = csv.writer(stream)
        csv_writer.writerow(routines.keys_from_schema(table))
        res = routines.fetch(f"SELECT * FROM {table};",
                from_file=False)
        for row in res:
            csv_writer.writerow(row)
archived = shutil.make_archive(zip_name, 'zip', tempdir)
print("created: ", end='')
print(repr(archived))
_ = input(f"<Enter> to delete {tempdir} ")
shutil. rmtree(tempdir)
