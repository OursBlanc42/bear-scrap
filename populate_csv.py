#!/usr/bin/env python3

"""
Save found posts to a CSV file.
"""

import csv


def save_found_posts(posts):
    # Save found posts to a CSV file

    with open("list.csv", "a") as f:
        writer = csv.writer(f)
        for post in posts:
            links_str = ", ".join(post.get('links', []))
            writer.writerow(
                [post['day'],
                 post['title'],
                 post['content'],
                 links_str,
                 post['text']])
    print("✅\tPosts saved successfully!")
