#!/usr/bin/env python3

"""
Read a CSV file and return a set of known posts (based on the 'day' field).

Returns:
    set: A set of known post based on the 'day' field.
"""

import csv


def read_csv():
    # Read found posts from a CSV file and return a set of known days

    known_posts = set()

    try:
        with open("list.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:  # Ensure row has enough columns
                    known_posts.add(row[0])  # Add day to set
    except FileNotFoundError:
        print("📄\tNo existing CSV file found, starting fresh...")

    print(f"✅\t{len(known_posts)} known posts loaded")
    return known_posts
