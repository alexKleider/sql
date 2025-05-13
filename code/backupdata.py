#!/usr/bin/env python3

# File: backupdata.py

"""
Copies data base,
Moves email json
Does _not_ deal with letters.
"""

import os
import shutil
import club
import helpers

now = helpers.timestamp4filename


src = club.db_file_name
dst = f"Secret/{now}.db"

def ck_existence(filename):
    if os.path.exists(filename):
        return True
    print("File 'filename' doesn't exist!")

def copy4backup(src, dst):
    while True:
        print("Options are Q)uit, C)opy, M)ove...")
        if not os.path.exists(src):
            print("Source file 'filename' doesn't exist!")
            return
        response = input(
                f"Q)uit, C)opy or M)ove {src} to {dst}?: ")
        if not response:
            continue
        else:
            if response[0] in 'cC':
                shutil.copyfile(src, dst)
                print(f"{src} copied to {dst}.")
                return
            elif response[0] in 'mM':
                shutil.move(src, dst)
                print(f"{src} moved to {dst}.")
                return
            elif response[0] in 'qQ':
                print("No action taken!")
                return


if __name__ == '__main__':
    for src, dst in (
            (club.db_file_name, f"Secret/{now}.db", ),
            (club.EMAIL_JSON, f"Secret/{now}.json", )
            ):
        copy4backup(src, dst)
