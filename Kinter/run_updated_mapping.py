#!/usr/bin/env python3

# File: run_updated_mapping.py

#import Kinter.collector
import Kinter.collector as collector
from code import helpers

def people():
    """provides a dict to be entered into the people table"""
    entries = {
            "First": "Joe",
            "Last": "Blow", 
            "Phone": "333/333-3333",
             }
    root_title = "User Info"
#   res = Kinter.collector.updated_mapping(entries, root_title)
    res = collector.updated_mapping(entries, root_title)

    if res:
        for key, value in res.items():
            print(f"{key}: {value}")
    else:
        print("people func returned None"

people()

