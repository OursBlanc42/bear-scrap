#!/usr/bin/env python3

"""
Read a CSV file and return a set of known posts (based on the 'day' field).

Returns:
    set: A set of known post based on the 'day' field.
"""

import csv
import os
from datetime import date

def find_current_year():
    # Find current year to generate one csv by year
    current_year = date.today().year
    return current_year

def save_found_posts(posts):
    # Save found posts to the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))

def read_csv():
    # Read found posts from a CSV file and return a set of known days
    known_posts = set()

    # Try to read the CSV file then check if it exists
    # If it does, read the 'day' field from each row and add it to the set
    try:
        # Get the directory of the current script and build the path to CSV
        script_dir = os.path.dirname(os.path.abspath(__file__))
        year = find_current_year()
        csv_path = os.path.join(os.path.dirname(script_dir), 'web', 'lists', f'list{year}.csv')

        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 1:
                    known_posts.add(row[0])
    except FileNotFoundError:
        print("📄\tNo existing CSV file found, starting fresh...")

    print(f"✅\t{len(known_posts)} known posts loaded")
    return known_posts
