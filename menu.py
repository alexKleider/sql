#!/usr/bin/env python3

# File: menu.py

"""
Top level rewrite using GUI
Goal is to replace main.py
"""

import sys
import PySimpleGUI as sg
from code import helpers
from code import routines
from code import commands
from code import data_entry
from code import ck_data
from code import show
from code import textual
from code import listings

hierarchy = {
    "Reports":{  # Text files created
        "4web": [show.show_cmd,],
        "applicants": [show.show_applicants_cmd,],
        "4exec": [commands.report_cmd,],
        "leadership": [commands.leadership_cmd,],
        "no email=>csv": [commands.no_email_cmd, ],
        "check_data_consistenchy":
                [ck_data.consistency_report, ],
        "sponsors": [listings.sponsors, ],
        "owing": [commands.still_owing_cmd,],
            },
    "Data Entry":{
        "Status Update": [data_entry.change_status_cmd],
            #Inserts or Updates a Person_Status table entry
        "New Applicant": [data_entry.add_new_applicant_cmd],
            #People, Applicant & Status tables
            #Google Contacts entry
        "Applicant (date) Update)": [
                    data_entry.update_applicant_date_cmd],
            #Applicant and Person_Status tables
        "Leadership Update (not implemented)": [],
            #Status table: term ending & beginning
            },
    "Prepare Mailing (under development)":{
        # populates email.json &/- MailingDir
        "First Notice (not implemented)": [],
        "June Request (not implemented)": [],
            },
    "Info":{  # csv files created
        "ZIP of CSV version of DB tables": [routines.db2csv],
        "Leadership (not implemented)": [],
        "Owing (not implemented)": [],
        "Receipts (not implemented)": [],
        "No Email (need letter) (not implemented)": [],
            },
        }

def main_menu(report=None):
    """
    Returns a list of functions (usually a list of only one.)
    Provides choices based on what's in <hierarchy>.
    """
    routines.add2report(report,
            "Begin main_menu...")
    options = [key for key in hierarchy.keys()]
    layout = [
        [sg.Text("Make a Choice", size=(30,1),)],
        [sg.Listbox(values=options, select_mode='extended',
            key='CHOICE', size=(30, len(options)))],
        [sg.Button('SELECT',), sg.Button('CANCEL'),]
            ]
    win = sg.Window("Main Menu", layout)
    e, v = win.read()
    win.close()
#   routines.add2report(report,
#           f"e: {repr(e)}, v: {repr(v)}")
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        routines.add2report(report,
            "Cancelled or no choice made; aborting main menu",
            also_print=True)
        return
    hkey = v['CHOICE'][0]  # hkey: hierarchy key
    
    options = [key for key in hierarchy[hkey].keys()]
    layout = [
        [sg.Text("Make a Choice", size=(30,1),)],
        [sg.Listbox(values=options, select_mode='extended',
            key='CHOICE', size=(30, len(options)))],
        [sg.Button('SELECT',), sg.Button('CANCEL'),]
            ]
    win = sg.Window(f"{hkey} Menu", layout)
    e,v = win.read()
    win.close()
#   routines.add2report(report,
#           f"e: {repr(e)}, v: {repr(v)}")
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        routines.add2report(report,
            "Cancelled or no choice made; aborting sub menu",
            also_print=True)
        return
    skey = v['CHOICE'][0]  # skey: sub-hierarchy key
    return f"{hkey}", f"{skey}"


if __name__ == "__main__":
#   print(f"Running {helpers.get_os_release()}")
#   print()
#   if not textual.yes_no(
#           f"Running {helpers.get_os_release()}",
#           title="Continue?"):
#       sys.exit()
    while True:
        report = []
        res = main_menu(report=report)
        if res:
            func_names = []
            for func in hierarchy[res[0]][res[1]]:
               routines.add2report(report,
                    f"executing {func.__name__}",
                    also_print=True)
               func_names.append(func.__name__)
               func(report)
        else:
            print("No choice made.")
            break
        file_name = (helpers.eightdigitdate + '-'
                    + "_".join(func_names)
                    + ".txt")
        yn = input(
            f"Send results to {file_name}? (y/n or other name) ")
        if len(yn) > 1:
            file_name = yn
        if yn and yn in {'n', 'N'}:
            for line in report:
                print(line)
            break
        else:
            with open(file_name, 'w') as outf:
                for line in report:
                    outf.write(line+'\n')
            break

