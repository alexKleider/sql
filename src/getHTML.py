#!/usr/bin/env python3

# File: src/getHTML.py


import requests
import glbls

site_page = glbls.site_page
html_file = glbls.html_file
password = glbls.password

def get_page(url, filename, creds=("", password)):
   """
   Downloads the source HTML from a given URL and saves it to a file.

   Args:
       url (str): The URL of the web page.
       filename (str): The name of the file to save the HTML to.
   """
   try:
       response = requests.get(url, auth=creds)
       response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

       with open(filename, "w", encoding="utf-8") as f:
           f.write(response.text)
       print(f"HTML source downloaded successfully to '{filename}'")

   except requests.exceptions.RequestException as e:
       print(f"Error downloading HTML: {e}")



if __name__ == "__main__":
   get_page(site_page, html_file)

