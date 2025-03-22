#!/usr/bin/env python3

# File: utils/scan.py

"""
Data Structuring:
  master:
    dict keyed by 'code_file_names'
      values are dicts keyed by the 'defined function names'
master[filename][func_name][filename][list_of_locations]
"""

import sys

code_files = """ alchemy.py ap_update.py attrition.py backupdata.py
ck_data.py club.py commands.py content.py data_entry.py dates.py
dock_change.py emailing.py fees.py gates.py get_data_byID.py
helpers.py leadership.py listings.py members.py mta.py multiple.py
old_member.py review.py routines.py show.py textual.py """.split()


def find(item, text):
    """
    Splits (on "\n") text into a sequence of <lines>.
    Returns a list of tuples: line and column
    where text represented by <item> is found.
    """
    lines = text.split("\n")
    locations = []
    lineN = 0
    for line in lines:
        lineN += 1
        begin = 0
        while True:
            location = line.find(item+"(", begin)
            if location == -1: break
            locations.append((lineN, location))
            begin += (location + len(item))
    return locations

def collect_data():
    #print(code_files)
    master = dict()
    for f in code_files:
        with open("code/" + f, 'r') as stream:
            key = f"{stream.name}"
            master[key] = dict()
            for line in stream:
                b = line.find("def ")
                if b>-1:
                    e = line.find("(",b)
                    if e>-1:
                        master[key][line[b+4:e]] = dict()
#                               ^     ^^^^^^^^
#                               |    func_name
#                              file where func is defined

    for f in code_files:
        with open("code/" + f, 'r') as stream:
            text = stream.read()
            f_name = stream.name
        for key in master.keys():
            for func_name in master[key].keys():
                if f_name == key:  # file where function is defined
                    target = func_name
                else:
                    target = f.split('.')[0] + '.' + func_name
                finding = find(target, text)
                if finding:
                    master[key][func_name][f_name] = finding
    return master


def show(data):
    for key, value in data.items():
        print(f"{key}:")
        for k, v in value.items():
            print(f"\t{k}:")
            for kk, vv in v.items():
                print(f"\t\t{kk}: {vv}")

def exercise_find():
    """ Exercise 'find(item, lines)' """
    fname = "code/data_entry.py"
    target = "add2report"
    outf = "output.txt"
    with open(fname, 'r') as stream:
        text = stream.read()
    locations = find(target, text)
    with open(outf, "w") as stream:
        stream.write(", ".join([repr(location) for location in
                                locations]))
    print(f"Found '{target}' {len(locations)} times within {fname}")
    print(f"Results sent to {outf}.")

if __name__ == "__main__":
    show(collect_data())
#   exercise_find()
