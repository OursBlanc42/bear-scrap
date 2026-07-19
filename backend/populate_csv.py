#!/usr/bin/env python3

"""
This function appends new posts to the existing CSV file.
It assumes each post is a dictionary with keys 'day', 'title',
'links_project', 'links_more', and 'links_support'.
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
    year = find_current_year()
    csv_path = os.path.join(os.path.dirname(script_dir), 'web', 'lists', f'list{year}.csv')

    with open(csv_path, "a") as f:
        writer = csv.writer(f)
        for post in posts:
            writer.writerow(
                [post['day'],
                 post['title'],
                 post['description'],
                 post.get('links_project', ''),
                 post.get('links_more', ''),
                 post.get('links_support', '')])
    print("✅\tPosts saved successfully!")
