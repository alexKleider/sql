#!/usr/bin/env python3

# File: menu.py

"""
Top level rewrite using GUI
Goal is to replace main.py
"""

import PySimpleGUI as sg
from code import helpers
from code import routines
from code import commands
from code import data_entry
from code import show

hierarchy = {
    "Reports":{  # Text files created
        "4web": [show.show_cmd,],
        "applicants": [show.show_applicants_cmd,],
        "4exec": [commands.report_cmd,],
            },
    "Data Entry":{
        "Status Update": [data_entry.change_status_cmd],
            #Person_Status table Insert or Update an entry
        "New Applicant": [],
            #People, Applicant & Status tables
            #Google Contacts entry
        "Meeting/newMember Update": [],
            #Applicant and Person_Status tables
        "Leadership Update": [],
            #Status table: term ending & beginning
            },
    "Prepare Mailing":{  # email.json & MailingDir populated
        "First Notice": [],
        "June Request": [],
            },
    "Info":{  # csv files created
        "Leadership": [],
        "Owing": [],
        "Receipts": [],
        "No Email (need letter)": [],
            },
        }

def main_menu(report=None):
    """
    Returns a list of functions (usually a list of only one.)
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
    routines.add2report(report,
            f"e: {repr(e)}, v: {repr(v)}")
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        routines.add2report(report,
            "Cancelled or no choice made; aborting main menu")
        if report: print(report[-1])
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
    routines.add2report(report,
            f"e: {repr(e)}, v: {repr(v)}")
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        routines.add2report(report,
            "Cancelled or no choice made; aborting sub menu")
        if report: print(report[-1])
        return
    skey = v['CHOICE'][0]  # skey: sub-hierarchy key
    return f"{hkey}", f"{skey}"


if __name__ == "__main__":
    print(f"Running {helpers.get_os_release()}")
    print()
    while True:
        report = []
        yn = input("Continue? (y/n) ")
        if yn and yn[0] in 'yY':
            res = main_menu(report=report)
            if res:
                for func in hierarchy[res[0]][res[1]]:
                   func(report)
            else:
                print("No choice made.")
            yn = input("Print report (y/n) or file name: ")
            if yn:
                if yn[0] in 'yY':
                    for line in report:
                        print(line)
                else:
                    with open(yn, 'w') as outf:
                        for line in report:
                            outf.write(line+'\n')
        else:
            break
