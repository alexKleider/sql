#!/usr/bin/env python3

# File: menu.py

"""
Top level rewrite using GUI
Goal is to replace main.py
"""

hierarchy = {
    "Reports":{  # Text files created
        "4web": { },
        "applicants": { },
        "4exec": { },
            },
    "Data Entry":{
        "New Applicant": { },
            #People, Applicant & Status tables
            #Google Contacts entry
        "Meeting/newMember Update": { },
            #Applicant and Person_Status tables
        "Leadership Update": { },
            #Status table: term ending & beginning
            },
    "Prepare Mailing":{  # email.json & MailingDir populated
        "First Notice": { },
        "June Request": { },
            },
    "Info":{  # csv files created
        "Leadership": { },
        "Owing": { },
        "Receipts": { },
        "No Email (need letter)": { },
            },
        }

import PySimpleGUI as sg
from code import commands
from code import helpers

def main_menu():
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
#   print(f"e: {repr(e)}, v: {repr(v)}")
    if e == 'CANCEL' or not v or not v["CHOICE"]:
        print("Cancelled or no choice made; aborting")
        return
    # repr(v): {'CHOICE': ['Reports']}
    hkey = v['CHOICE'][0]  # hkey: hierarchy key
#   print(f"e: {repr(e)}, v: {repr(hkey)}")
    
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
    if e == 'CANCEL' or not v or not v["CHOICE"]:
#       print("Cancelled or no choice made; aborting")
        return
    skey = v['CHOICE'][0]  # skey: sub-hierarchy key
#   print(f"e: {repr(e)}, v: {repr(skey)}")
    return f"{hkey}", f"{skey}"


if __name__ == "__main__":
    print(f"Running {helpers.get_os_release()}")
    print()
    while True:
        yn = input("Continue? (y/n) ")
        if yn and yn[0] in 'yY':
            print(main_menu())
        else:
            break
