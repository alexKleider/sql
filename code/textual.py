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

def get_demographics(applicant=True, report=None):
    """
    Uses a GUI to collect all demographic data needed to create
    an entry into the People table AND (unless <applicant> is set
    to <False>) also collect two sponsor names and app_rcvd and
    fee_rcvd fields.
    Caution: do not hit the minimize button ([_] top right
    corner!) This causes the system to hang!!!
    Returns a dict or None (if user aborts.)
    Client is code/data_entry.py
    """
    routines.add2report(report,
            "Entering textual/get_demographics...")
    fields = routines.keys_from_schema("People", brackets=(1,0))
    if applicant==True:
        fields.extend(["sponsor1", "sponsor2", "app_rcvd", "fee_rcvd"])
    layout = [  # the entry fields...
            [sg.Text(f_name),
                sg.Input(expand_x=True, key=f_name)]
            for f_name in fields
            ]    #  ...now and two Buttons:
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window('Enter demographics', layout,
#               no_titlebar=True
                )
    event, values = window.read()
    window.close()
    if event in (None, 'Cancel'):
        routines.add2report(report,
                "... gui/get_demographics returning None.")
        return
    elif event == 'OK':
        data = values
        entry = ["... gui/get_demographics returning:"]
        for key, value in data.items():
            entry.append(f"\t{key}: {value}")
        routines.add2report(report, entry)
        return data
    else:
        assert False, f"!Unexpected event: {repr(event)}!"


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

def people_choices(header_prompt=None, report=None):
    """
    GUI method of getting a selected list of people from
    which to choose: returns a listing of ID, first, last tuples
    OR None.
    1st step in providing 
    code/routines/pick_People_record functionality!
    """
    routines.add2report(report,
            "Entering textual/people_choices...")
    # 1st collect the 'hints' ==> data:
    fields = routines.keys_from_schema(
                    "People", brackets=(1,7))
    layout = [[sg.Text(f_name), sg.InputText()]
                    for f_name in fields  ]
    layout.append([sg.Button('OK'),
                        sg.Button('Cancel')])
    window = sg.Window(
        'Enter hints using "%" as wild cards:',
                                    layout)
    data = None
    event, values = window.read()
    if event == 'OK':
#       print("event OK, set(values.values()): " +
#           f"{repr(set(values.values()))}") 
        if set(values.values()) == {''}:  # all empty strings
            report.append("Got an empty list ==> returning None")
            return
        data = {}
        for n in range(len(values)):
            data[fields[n]] = values[n]
    elif event in (None, "Cancel"): 
        report.append(
                f"event: {repr(event)} ==> returning None")
        return
    else:
        assert False, f"Unexpected event: {repr(event)}"
    window.close()
    # report prn (expect to redact this section...
    routines.add2report(report, "First window returning:")
    for key, value in data.items():
        routines.add2report(report,
                f"key: {key}   value: {value}")
    # use hints to get candidates:
    query_lines = [
        "Select personID, first, last, suffix",
            "from People where ", ]
    additional_lines = []
    if data['first']:
        additional_lines.append(
            f"""first like "{data['first']}" """)
    if data['last']:
        additional_lines.append(
            f"""last like "{data['last']}" """)
    if data['suffix']:
        additional_lines.append(
            f"""suffix like "{data['suffix']}" """)
    additional_lines = " AND ".join(additional_lines)
    query_lines.append(additional_lines)
    query = ' '.join(query_lines)
    query = query+';'
#   _ = input(f"query is {repr(query)}")
    ret = routines.fetch(query, from_file=False)
    routines.add2report(report, "query returning:")
    for item in ret:
        routines.add2report(report, repr(item))
    return ["{0!s:>3} {1:} {2:} {3:}".format(*item) 
            for item in ret]


def choose(choices, header="CHOOSE ONE",
                    subheader="Pick a person",
                    report= None):
    """
    Returns one of the <choices> (a list of strings)
    or something that'll evaluate to False
    Adds to <report> (a list of strings) if provided.
    """
    #set the theme for the screen/window
    routines.add2report(report,
            "Entering code.textual.choose")
    if not choices:
        routines.add2report(report,
                "No choices provided ==> exit")
        return
#   sg.theme('SandyBeach')
    layout=[[sg.Text(subheader,size=(30,1),
#           font='Lucida',justification='left'
            )],
            [sg.Listbox(values=choices, select_mode='extended',
                key='CHOICE', size=(30,len(choices)))],
            [sg.Button('SELECT',
#               font=('Times New Roman',12)
                ),
            sg.Button('CANCEL',
#                   font=('Times New Roman',12)
                    )
            ]]
    win =sg.Window(header,layout)
    e, v = win.read()
    win.close()
    routines.add2report(report,
            f"Window returning e: {repr(e)}, v: {repr(v)}")

    if (e != "SELECT") or not v['CHOICE']:
        routines.add2report(report, "Returning None")
        return
    else:
        routines.add2report(report,
          f"code.textual.choose returning {repr(v['CHOICE'])}")
        return v['CHOICE']


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

def test_choose():
    options =['1 Alex Kleider',
            '2 Randy Rush',
            '3 Don Murch', ]
    while True:
        yn = input("\nRun test_choose? (y/n)")
        report = []
        if yn and yn[0] in 'yY':
            ret = choose(options, report=report,
                        header="[X] to abort, CANCEL to begin again",
                        subheader="Select your choice.")
            for line in report: print(line)
        else:
            break


def pick_person(header="CHOOSE ONE",
                subheader="Pick a person"):
    """
    Returns a person record from the People table
        or None if user chooses to abort using [X].
    Used to obtain a record
    [X] ==> Returns None
    CANCEL ==> goes around again
    empty list ==> same as CANCEL
    If all goes according to plan:
    """
    while True:
        start_over = False
        # 1st collect the 'hints' ==> data:
        fields = routines.keys_from_schema(
                        "People", brackets=(1,7))
        layout = [[sg.Text(f_name), sg.InputText()]
                        for f_name in fields  ]
        layout.append([sg.Button('OK'),
                            sg.Button('Cancel')])
        window = sg.Window(
            'Enter hints using "%" as wild cards:',
            layout)
        while True:
            data = None
            event, values = window.read()
            print(f"event: {repr(event)}")
            if event == 'OK':
                if not values:  # could be an empty list
                    print("Got an empty list; try again.")
                    continue
                data = {}
                for n in range(len(values)):
                    data[fields[n]] = values[n]
                break  # got what we want!
            elif event == None:  # when user hits the [X]
                return
            elif event == 'Cancel':
                start_over = True
                break
            else:
                print("Unexpected event!")
                assert False
        window.close()
        if start_over: continue
        query_lines = [
            "Select personID, first, last, suffix",
                "from People where ", ]
        additional_lines = []
        if data['first']:
            additional_lines.append(
                f"""first like "{data['first']}" """)
        if data['last']:
            additional_lines.append(
                f"""last like "{data['last']}" """)
        if data['suffix']:
            additional_lines.append(
                f"""suffix like "{data['suffix']}" """)
        if not additional_lines:
            print("No clues provided; going again")
            continue
        additional_lines = " AND ".join(additional_lines)
        query_lines.append(additional_lines)
        query = ' '.join(query_lines)
        query = query+';'
#       _ = input(query)
        ret = routines.fetch(query, from_file=False)
        if not ret: continue
#       _ = input(repr(ret))
#       for item in ret:
#           print(item)
        choices = ["{0!s:>3} {1:} {2:} {3:}".format(*item) 
            for item in ret]

        #define layout
        layout=[[sg.Text(subheader,size=(30,1),
                )],
                [sg.Combo(choices,
                    default_value=choices[0],
                    key='choice')],
                [sg.Button('SELECT',
                    ),
                sg.Button('CANCEL',
                        )
                ]]

#       layout=[[sg.Text(choice), sg.InputText()]
#               for choice in choices]
#       layout.append([sg.Button('OK'),
#           sg.Button('Cancel')])
        #Define Window
        win =sg.Window(header,layout)
        #Read  values entered by user
        e, v = win.read()
        #close first window
        win.close()
        #access the selected value in the list box
        #and add them to a string
#       print(f"e returns {e}")
        if e == "CANCEL":
            continue
        elif e == None:
            return
        else:
    #       print("you chose: ",end='')
    #       print(repr(v['choice']))
            return routines.get_rec_by_ID(
                int(v['choice'].split()[0]))

def test_pick_person():
    while True:
        record = input(repr(pick_person()))
        print(repr(record))
        yn = input("Continue? (y/n) ")
        if not (yn and yn[0] in 'yY'):
            break

def test_people_choices():
    report = []
    res = people_choices(report=report,
        header_prompt = "Choose from the People table...")
    if not res:
        print(f"people_choices returned {repr(res)}")
    else:
        print("pick_Poeple_record returning the following...")
        for item in res:
            print(f"{repr(item)}")
    print("\nReport follows...")
    print('\n'.join(report))



if __name__ == "__main__":
#   test_people_choices()
#   get_demographics(report=report,
#           applicant=False)
#   test_pick_person()
#   test_create_dem_file()
#   main1()
    test_choose()

