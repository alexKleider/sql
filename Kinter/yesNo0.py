#!/usr/bin/env python3

# File: Kinter/yesNo0.py

import tkinter as tk
from tkinter import messagebox
from tkinter import font

header = "Accept data?"
question ="""
Multi line
message
goes here
"""

# Create the main application window (it can be hidden if only the dialog is needed)
root = tk.Tk()
root.withdraw() # Hides the main window, showing only the dialog
###########
# Get the existing TkCaptionFont object
caption_font = font.nametofont("TkCaptionFont")

# Configure the font family and size
caption_font.config(family="Arial", size=24) 

# Set the message body font as well for consistency
root.option_add('*Dialog.msg.font', 'Arial 12')
###########

def show_yes_no_box(header=header,
                    question=question):
    # Show the yes/no message box and store the result
    # The first argument is the dialog title, the second is the message
    result = messagebox.askyesno(header, question)

    if result == True:
        # User clicked 'Yes'
        print("User clicked Yes. Exiting application.")
        root.destroy() # Closes the application
    else:
        # User clicked 'No'
        print("User clicked No. Staying in application.")
        messagebox.showinfo("Return", "Returning to main application")

# Call the function to display the dialog box
if __name__ == "__main__":
    show_yes_no_box()


