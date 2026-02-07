#!/usr/bin/env python3

# File: topLevel.py

"""
The primary top-level widgets in Tkinter are
    the root window (Tk) and
    `Toplevel windows.

Tkinter Top-Level Widgets
=========================
These widgets serve as the foundation for the entire GUI
application and cannot be placed inside other containers.

Tk
--
This is the main application window (often referred to
as the root window) and must be instantiated only once per
application. All other widgets are contained within or
associated with this root instance.

Toplevel
--------
This widget is used to create separate, independent
sub-windows that are managed by the window manager, distinct
from the main Tk window. They are often used for dialog boxes,
pop-up windows, or secondary application windows.
"""

import tkinter as tk

def open_toplevel_window():
    """Creates and displays a new Toplevel window."""
    # 1. Create the Toplevel widget, specifying the parent (root)
    new_window = tk.Toplevel(root)
    new_window.title("New Toplevel Window")
    new_window.geometry("300x200") # Optional: set initial size

    # 2. Add widgets to the Toplevel window, just like the main window
    label = tk.Label(new_window, text="This is a new window!")
    label.pack(pady=10)

    # 3. Add a button to close the Toplevel window
    close_button = tk.Button(new_window, text="Close Window", command=new_window.destroy)
    close_button.pack(pady=10)
    
    # Optional: Make the Toplevel window a modal dialog
    # This prevents interaction with the main window until the Toplevel window is closed.
    # new_window.grab_set()

# Create the main application window
root = tk.Tk()
root.title("Main Window")
root.geometry("450x300")

# Add widgets to the main window
main_label = tk.Label(root, text="This is the main window")
main_label.pack(pady=20)

# Add a button in the main window to open the Toplevel window
open_button = tk.Button(root, text="Open New Window", command=open_toplevel_window)
open_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()



