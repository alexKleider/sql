#!/usr/bin/env python3

# File: try.py


import json

data = {
    "name": "Alice",     "age": 30,
    "city": "New York",
    "interests": ["reading", "hiking", "cooking"]
}

# Compact representation (default)
compact_json = json.dumps(data)
print("Compact JSON:")
print(compact_json)

# Pretty-printed with 4 spaces indentation
pretty_json_spaces = json.dumps(data, indent=4)
print("\nPretty-printed JSON (4 spaces):")
print(pretty_json_spaces)


# Pretty-printed with tab indentation
pretty_json_tabs = json.dumps(data, indent='\t')
print("\nPretty-printed JSON (tabs):")
print(pretty_json_tabs)

# Writing to a file with indentation
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
with open("output.json", 'r') as f:
    data = json.load(f)
print(json.dumps(data))

redact = '''    

print(json.dumps(data, indent=2))
print("=============================")
with open("output.json", 'r') as f:
    data = json.load(f)
print(data)
pretty_json = json.dumps(data, indent=4)
print(pretty_json)

'''
