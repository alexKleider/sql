#!/usr/bin/env python3

# File: Kinter/check.py

"""
Opens two windows! 
"""

import tkinter as tk
from tkinter import font as tkFont

def on_closing():
    root.destroy()
#   if messagebox.askokcancel("Quit", "Really want to quit?"):
#       root.destroy()

def custom_message_box(title_text, message_text):
    popup = tk.Toplevel()
    popup.wm_title(title_text)
    # Optional: make it modal (disable the main window while the popup is open)
    popup.grab_set()

    # Define a custom font for the 'header' label within the dialog
    header_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

    # Create the title/header label
    title_label = tk.Label(popup, text=title_text, font=header_font, pady=10, padx=10)
    title_label.pack(side="top", fill="x")

    # Create the message content label
    message_label = tk.Label(popup, text=message_text, font=("Arial", 14), pady=10, padx=10)
    message_label.pack(side="top", fill="x")

    # Add an OK button to close the popup
#   ok_button = tk.Button(popup, text="OK", command=popup.destroy, pady=5)
    ok_button = tk.Button(popup, text="OK", command=root.destroy, pady=5)
    ok_button.pack(side="bottom", pady=10)

    # Center the dialog on the screen (basic method)
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))
#   root.destroy()

# Example usage:
root = tk.Tk()
#root.withdraw() # Hide the main window
root.protocol("WM_DELETE_WINDOW", on_closing)
custom_message_box("Custom Header", "This entire window has custom fonts.")
root.mainloop()

