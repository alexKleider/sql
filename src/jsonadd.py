#!/usr/bin/env python3

# File: jsonadd.py

"""
Code from AI: to examine, modify and possibly use
to replace equivalent code in code/routines.py
"""

import json

def append_to_json_file(jfile, new_data):
    """
    Appends new_data (a dictionary or a list of dicts) to a JSON
    file containing a list of dictionaries.
    If the file doesn't exist or is empty, it initializes it
    with a list containing new_data.
    """
    try:
        with open(jfile, 'r+') as f:  # 'r+' == read & write #
            # Retrieve existing data
            try:
                file_data = json.load(f)
            except json.JSONDecodeError:  # Handle empty or invalid JSON file
                file_data = []

            # Ensure file_data is a list before appending
            if not isinstance(file_data, list):
                # If it's not a list, wrap it in a list or handle as appropriate
                file_data = [file_data] 

            # Append new data
            file_data.append(new_data)

            # Go to the beginning of the file and write the updated data
            f.seek(0)
            json.dump(file_data, f, indent=4)
            f.truncate() # Remove remaining old content if new content is shorter

    except FileNotFoundError:
        # If the file doesn't exist, create it with the new data as a list
        with open(jfile, 'w') as f:
            json.dump([new_data], f, indent=4)

# Example usage:
file_name = "my_data.json"
new_entry = {"name": "Alice", "age": 30, "city": "New York"}
another_entry = {"name": "Bob", "age": 25, "city": "London"}

append_to_json_file(file_name, new_entry)
append_to_json_file(file_name, another_entry)

# To verify the content:
with open(file_name, 'r') as f:
    data = json.load(f)
    print(data)
