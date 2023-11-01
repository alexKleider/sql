#!/usr/bin/env python3

# File: gui.py

""" Gui-like interface:
Using pysimplegui @
https://www.pysimplegui.org/en/latest/#github-statistics
(See also https://textual.textualize.io/getting_started/
as a possible alternative.)
"""

import PySimpleGUI as sg

try: from code import routines
except ImportError: import routines
try: from code import helpers
except ImportError: import helpers

def get_demographics(report=None):
    """
    Uses a GUI to collect an entry for the People table.
    Returns a dict or None if no entry.
    """
    routines.add2report(report,
            "Entering gui/get_demographics...")
    fields = routines.keys_from_schema("People", brackets=(1,0))
    layout = [  # the entry fields...
            [sg.Text(f_name), sg.InputText()]
            for f_name in fields
            ]    #  ...now and two Buttons:
    layout.append([sg.Button('OK'), sg.Button('Cancel')])
    window = sg.Window('Enter demographics', layout)

    # Create the event loop
    while True:
        data = None
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'OK':  # create a dict
            data = {}
            for n in range(len(values)):
                data[fields[n]] = values[n]
            break

    window.close()
    if report:
        if data:
            entry = ["... gui/get_demographics returning:"]
            for key, value in data.items():
                entry.append(f"")
        else:
            entry = "... gui/get_demographics returning None."
    routines.add2report(report, entry)
    return data

def create_dem_file(data, report=None):
    """
    Creates a "flDem.txt" file.
    Uses data collected by get_demographics()
    to create a text file showing the data collected.
    Differs from a Secret/flAp.txt file in that
    sponsor data is missing.
    """
    record = helpers.Rec(data)
    for key, value in record.items():
        print(f"key: {key},  value: {value}")
    fname = ('Secret/Applicants/' +
            record['first'][0].lower() +
            record['last'][0].lower() +
            record['suffix'] +
            'Dem.txt')  # No sponsor data included!!
    if not record['suffix']:
        record['suffix'] = 'No Suffix'
    with open(fname, 'w') as outf:
        outf.write(f"# File: {fname}\n")
        outf.write(
          f"# {record['first']} {record['last']} " +
          f"{record['suffix']} {helpers.date}\n")
        outf.write("\n")
        for key, value in record.items():
            if key == 'suffix':
                if not value:
                    outf.write("No Suffix\n")
                else:
                    outf.write(value+'\n')
            else:
                outf.write(value+'\n')



def test_create_dem_file():
    data = dict(
      first= "Alex",
      last= "Kleider",
      suffix=  "",
      phone= "phone",
      address= "street",
      town= "Bo",
      state= "CA",
      postal_code= "94924",
      country= "usa",
      email= "alex@kleider.ca",
      )
#   for key, value in data.items():
#       print(f"  {key}: {value}")
    report=['creating dem file',]
    create_dem_file(data, report=report)
    print(report)


def main1():
    report = ['Report: ', ]
    data = get_demographics(report=report)
    if data:
        print("Data collected:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        _ = input("To continue hit the 'Enter' key... ")
    else:
        print("no data entered")
    yn = input("Create a '..Dem.txt' file? (y/n) ")
    if yn and yn[0] in "yY":
        create_dem_file(data, report=report)

if __name__ == "__main__":
    test_create_dem_file()

