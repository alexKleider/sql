#!/usr/bin/env python3

# File: interface.py

import tkinter as tk
from tkinter import ttk

"""
Listing of ../../TK directory:
choose_text.py  club.db  collector.py  helpers.py  __pycache__  routines.py  tkUINotes.txt  UselessTK
click.py        club.py  func_menu.py  Notes       README       textual.py   ToDo           yn.py

Requires a mapping of text: function key/values.
Provides a menu and executes the function pertaining
to the key chosen.
"""

import tkinter as tk

def func_menu(funcs):
    def show_page(page_name):
    #   # Logic to switch views or print selection
    #   label.config(text=f"Currently viewing: {page_name}")
    #   my code:
        print(f"function name: func.name")
        root.destroy()
    def destroyer(func):
        def wrapper(*args, **kwargs):
            res = func()
            root.destroy()
        return wrapper

    root = tk.Tk()
    root.title("Vertical Menu Example")
    root.geometry("400x300")

    # 1. Sidebar Frame
    sidebar = tk.Frame(root, bg="#2c3e50", width=150, height=300)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False) # Prevents frame from shrinking to button size

    # 2. Menu Buttons (Vertical Items)
    #menu_items = ["Dashboard", "Settings", "Profile", "Help"]
    #for item in menu_items:
    for func in funcs:
        # decorate each function to include root.destroy() 
        btn = tk.Button(
            sidebar, 
            text=func.__name__, 
            command= destroyer(func),
                    # ...decorate with a root.destroy() line
            bg="#2c3e50", 
            fg="white", 
            activebackground="#34495e", 
            activeforeground="white",
            bd=0, 
            padx=20, 
            pady=10, 
            anchor="w")
#       print(f"assigned {func.__name__}")
        btn.pack(fill="x") # Ensures buttons take full width of sidebar

    # 3. Main Content Area
    main_area = tk.Frame(root, bg="white")
    main_area.pack(side="right", expand=True, fill="both")

    label = tk.Label(main_area,
                     text="Select an option from the menu",
                     bg="white")
    label.pack(pady=50)

    root.mainloop()

def ck_func_menu():
    def func1():
        print(f"Executing func1")
    def func2():
        print(f"Executing func2")
    def func3():
        print(f"Executing func3")
    funcs = (func1, func2, func3, )
    
    func_menu(funcs)

if __name__ == "__main__":
    ck_func_menu()
