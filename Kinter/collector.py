#!/usr/bin/env python3

# File: collector.py

import tkinter as tk

""" Provides function <updated_mapping>.  """

global_res = {}  # collects info from the gui window

def updated_mapping(entries, root_title="Record Update"):
    """
    Provides a way of entering or modifying the values of a
    <mapping>, presented in a window labeled <root_title>.
    Returns None if closed without using the submit button.
    The <submit> button causes return of a new mapping with
    the visible values. The original mapping is left unchanged.
    Retrieval depends on <global_res> which must exist globally.
    """
    def submit_data():
        global global_res
        for key in entries.keys():
            global_res[key] = str_vars[key].get()
        root.destroy()

    root = tk.Tk()
    root.title(root_title)

    keys = entries.keys()
    labels = {}
    str_vars = {}
    values = {}

    row = 0;

    for key, value in entries.items():
        labels[key] = tk.Label(root, text=key)
        labels[key].grid(row=row, column=0)
        str_vars[key] = tk.StringVar(value=value)
        values[key] = tk.Entry(root, textvariable=str_vars[key])
        values[key].grid(row=row, column=1)
        row += 1;

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit_data)
    submit_button.grid(row=row, column=1)

    root.mainloop()
#   print (f"{res=}")
    return global_res


def run_updated_mapping():
    entries = {
            "First": "Joe",
            "Last": "Blow", 
            "Phone": "333/333-3333",
             }
    root_title = "User Info"
    res = updated_mapping(entries, root_title)
    print(f"{res=}")
    if res:
        for key, value in res.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    run_updated_mapping()

