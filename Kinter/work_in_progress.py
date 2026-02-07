#!/usr/bin/env python3

# File: work_in_progress.py

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

window = Toplevel(root)
response = messagebox.askyesno("Confirmation",
                "Do you want to save changes?")
print(f"{response=}")


root.mainloop()

