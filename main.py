#!/usr/bin/env python3

# File: main.py

"""
Main driver of SQL version of
             the
    Bolinas Rod & Boat Club
          Membership
data management software.
Support code found in the 'code' directory.
'code/routines.py' contains helper functions.
'code/commands.py': the commands themselves.
    so far: just working on 'show_cmd'
        which generates output for the web site.
"""

import sys
from code import commands


def main():
    cmd = None
    args = []
    largs = len(sys.argv)
    if largs > 1:
        args = sys.argv[2:]
        cmd = sys.argv[1]
        if cmd == 'show': cmd = commands.show_cmd
        elif cmd == 'applicants': cmd = commands.appl_cmd
        else: cmd = None
    else: 
        cmd = commands.get_command()
    if cmd: 
        res = cmd()
        if args:
            outfile = args[0]
        else:
            outfile = input("Send result to file: ")
        with open(outfile, 'w') as outstream:
            outstream.write(res)
            print(f"Results sent to {outstream.name}.")
    else:
        print("No valid command provided.")


if __name__ == '__main__':
    main()

