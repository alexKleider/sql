#!/usr/bin/env python3

# File: close.py

"""
Hitting [x] on root window closes the application.
"""

import tkinter as tk

def on_closing():
    """This function is called when the user attempts to close the window."""

    print("Window is closing. Performing cleanup...")
    # Add any cleanup code here (e.g., saving data, closing connections)
    root.destroy() # This actually closes the window and stops mainloop

root = tk.Tk()
root.title("WM_DELETE_WINDOW Example")
root.geometry("300x200")

# Bind the window close event to the custom on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Add some widgets (optional)
label = tk.Label(root, text="Click the 'X' button to see custom handling.")
label.pack(pady=50)

root.mainloop()

