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

Some development is taking place in utilities.py
"""

from code import commands

if __name__ == '__main__':
    yn = input("Do you wish to see a report? (y/n): ")
    # 2do: report has to do with program progress
    #      data file output should be made independent of it.
    report = ["Report generated using "]
    report.append("=" * len(report[0]))
    while True:
        cmd = commands.get_command()
        print(f"got a command: {cmd.__name__}")
        if cmd: 
            print("checking if want a report...")
            if yn and yn[0] in 'Yy':
                res = cmd(report=report)
                outfile = input(
                "Send report to file (blank if to StdOut:) ")
                if outfile:
                    with open(outfile, 'w') as outstream:
#                       outstream.write('\n'.join(res))
                        outstream.write('\n'.join(report))
                        print(
                            f"Results sent to {outstream.name}.")
                else:
                    print(
                        "No file selected; output to stdout...")
                    for line in res:
                        print(repr(line))
            else:
                print(
                  "...running command without generating a report.")
                res = cmd()
        else:
            print("No valid command provided.")
        response = input(
            "\n Q)uit or any other key to continue... ")
        if response and response[0] in 'qQ': break 

