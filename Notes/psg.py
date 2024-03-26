#!/usr/bin/env python3

# File: psg.py

"""
Coding Conventions:
    import PySimpleGUI as sg
    sg.popup('This is a popup')
    if event == 'Ok':
        name = values['-NAME-']
https://docs.pysimplegui.com/en/latest/documentation/quick_start/groups_of_apis/
Two groups of functions & objects within PySimpleGUI:
    Windowing Focused APIs
    Supporting APIs
Windowing APIs: classes and function calls used
    to put something visually on the screen.
    The windowing APIs can be further divided into two categories
        "Popup" Windows - super-easy, single-line function calls that display a window
        Custom Windows - objects and functions to help you make windows you have complete control over
        System Tray - access to the system tray so your program can run in the background and still be accessable
Supporting APIs: objects and functions that help with your entire application.
"""

import PySimpleGUI as sg   # simple GUI

# output:
sg.popup("Hello universe...I'm a 1-line GUI program!")
# 19 additional optional params!
# popup_animated
# popup_annoying
# popup_auto_close
# popup_cancel
# popup_error
# popup_error_with_traceback
# popup_get_date
# popup_get_file
# popup_get_folder
# popup_get_text
# popup_menu
# popup_no_border
# popup_no_buttons
# popup_no_frame
# popup_no_titlebar
# popup_no_wait
# popup_non_blocking
# popup_notify
# popup_ok
# popup_ok_cancel
# popup_quick
# popup_quick_message
# popup_scrolled
# popup_timed
# popup_yes_no
if sg.popup_yes_no("OK to proceed?",
        no_titlebar=True)=="Yes":
    print("Yes")
else:
    print("No")


# sg.popup_no_titlebar()
# sg.popup('I do not have a titlebar.', no_titlebar=True)
# sg.popup_no_titlebar('I do not have a titlebar.')

# input:
#name = sg.popup_get_text('What is your name?')
#print(name)
# print to the debug window
#sg.Print("Hello multiverse!?", colors='white on red')
# one line progress meter
#for i in range(0, 100):
#    sg.one_line_progress_meter("Just as the name says", i, 99)

