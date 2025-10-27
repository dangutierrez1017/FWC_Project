"""
database_loader.py
------------------
Handles all data ingestion for the FWRI KeyCard Entry Database.
This module loads data from JSON files into memory
in the form of Python Dictionaries.

Author: Daniel Gutierrez
Date: 10/22/2025
"""


import json

def load_employees_json():
    """Load employee data from the assets directory."""
    with open('assets/employees.json') as f:
        employees = json.load(f)
    return employees

def load_keyCard_Entries():
    """Load keycard entry logs."""
    with open('assets/keycardentries.json') as f:
        keycard_entries = json.load(f)
    return keycard_entries

def load_images_json():
    """Load security camera image metadata."""
    with open('assets/images.json') as f:
        images = json.load(f)
    return images

def load_categories_json():
    """Load image category data."""
    with open('assets/categories.json') as f:
        categories = json.load(f)
    return categories

