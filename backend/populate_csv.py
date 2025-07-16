#!/usr/bin/env python3

"""
This function appends new posts to the existing CSV file.
It assumes each post is a dictionary with keys 'day', 'title',
'links_project', 'links_more', and 'links_support'.
"""

import csv
import os


def save_found_posts(posts):
    # Save found posts to a CSV file
    # Get the directory of the current script and build the path to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'data', 'list.csv')

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
