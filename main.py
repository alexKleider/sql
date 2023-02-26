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

See code/commands/get_command() for what's so far implemented.
"""

import sys
from code import commands


def main():
    """
    Too complicated! needs debugging!!
    """
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
        if outfile:
            with open(outfile, 'w') as outstream:
                outstream.write('\n'.join(res))
                print(f"Results sent to {outstream.name}.")
        else: print('\n'.join(res))
    else:
        print("No valid command provided.")


if __name__ == '__main__':
    while True:
        cmd = commands.get_command()
        if cmd: 
            res = cmd()
            outfile = input("Send result to file: ")
            if outfile:
                with open(outfile, 'w') as outstream:
                    outstream.write('\n'.join(res))
                    print(f"Results sent to {outstream.name}.")
            else:
                print("No file selected; output to stdout...")
                print('\n'.join(res))
        else:
            print("No valid command provided.")
        response = input("....continue? ")
#       if response and response[0] in 'nN':
#           break

