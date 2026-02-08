#!/usr/bin/env python3

# File: try.py

import tkinter as tk
from tkinter import messagebox

def on_closing():
    """
    Function called when the user clicks the window manager's close button.
    Prompts for confirmation before closing the window.
    """
    root.destroy() # Closes the main window
#   if messagebox.askokcancel("Quit", "Do you really want to quit?"):
#       root.destroy() # Closes the main window

# Create the main window
root = tk.Tk()
root.title("Custom Close Behavior")
root.geometry("400x300")

# Bind the on_closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Add a simple label to the window
#label = tk.Label(root, text="Click the 'x' to see the custom behavior.")
#label.pack(pady=50)

# Run the Tkinter event loop
root.mainloop()
