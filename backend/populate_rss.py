#!/usr/bin/env python3

"""
Those functions recreate the RSS file from CSV or during scraping.
It assumes each post is a dictionary with keys 'day', 'title',
'links_project', 'links_more', and 'links_support'.
"""

import rfeed
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

def save_found_posts_in_rss(posts):
    # Save found posts to a RSS file
    # Get the directory of the current script and build the path to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rss_path = os.path.join(os.path.dirname(script_dir), 'web', 'feed.rss')
    load_dotenv(dotenv_path=os.path.join(script_dir, '.env'))

    items_ = []
    for post in posts:
        main_link = post.get('links_project', post.get('links_more', post.get('links_support', ''))),
        item = rfeed.Item(
            title=post['title'],
            link=main_link,
            description=post['description'],
            guid=rfeed.Guid(main_link),
        )
        items_.append(item)

    feed = rfeed.Feed(
        title="Les Logiciels Libres de l'été",
        description="Découvrez les projets Open Source présentés par Bearstech",
        language="fr-FR",
        items=items_,
        lastBuildDate=datetime.now(),
        link=os.getenv('APP_URL')
    )

    with open(rss_path, "w") as f:
        f.write(feed.rss())

    print("✅\tRSS updated successfully!")


def build_rss_from_csv():
    # Build RSS file from generated CSV file
    # Get the directory of the current script and build the path to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(dotenv_path=os.path.join(script_dir, '.env'))
    csv_path = os.path.join(os.path.dirname(script_dir), 'web', 'list.csv')
    rss_path = os.path.join(os.path.dirname(script_dir), 'web', 'feed.rss')
    items_ = []

    with open(csv_path, "r") as c:
        reader = csv.reader(c)
        for row in reader:
            main_link = row[5] if not row[4] else row[4] if not row[3] else row[3],
            item = rfeed.Item(
                title=row[1],
                link=main_link,
                description=row[2],
                guid=rfeed.Guid(main_link),
            )
            items_.append(item)

    feed = rfeed.Feed(
        title="Les Logiciels Libres de l'été",
        description="Découvrez les projets Open Source présentés par Bearstech",
        language="fr-FR",
        items=items_,
        lastBuildDate=datetime.now(),
        link=os.getenv('APP_URL')
    )

    with open(rss_path, "w") as f:
        f.write(feed.rss())

    print("✅\tRSS updated successfully!")