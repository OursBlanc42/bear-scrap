#!/usr/bin/env python3

"""
Main script to scrape LinkedIn posts from the BearsTech page.

This script logs into LinkedIn, navigates to the BearsTech page,
and scans for posts related to "Les Logiciels Libres de l'été".
It saves the found posts to a CSV file and avoids duplicates
by checking against previously saved posts.
"""

# Import libraries
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import re
import time
import traceback
import os
from populate_csv import save_found_posts
from read_csv import read_csv
from datetime import datetime

# Execution time calculation
start_time = time.time()

# Load configuration from config file
config = configparser.ConfigParser()
# Get the directory of the current script and build the path to config
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config')
config.read(config_path)
email = config.get('credential', 'email')
password = config.get('credential', 'password')

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=options)

# Read known posts from CSV
known_posts = read_csv()

try:
    # Go to LinkedIn login page
    print("🌐\tNavigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")

    # Wait for the login form to load
    wait = WebDriverWait(driver, 10)

    # Find and fill email field
    print("✉️\tFilling the email field...")
    email_field = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(email)

    # Find and fill password field
    print("🔑\tFilling the password field...")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Find and click login button
    print("🔓\tClicking the login button...")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for login to complete (wait for redirect or main page element)
    print("⏳\tWaiting for login to complete...")
    wait.until(
        EC.url_contains("linkedin.com/feed") or
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    )
    print("✅\tLogin successful!")

    # Now navigate to the desired page
    print("🐻\tNavigating to BearsTech page...")
    bearstech_url = "https://www.linkedin.com/company/bearstech/posts/"
    driver.get(f"{bearstech_url}?feedView=all")

    # Wait for the page content to load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    print("🌐\tSuccessfully arrived on the BearsTech page!")

    # Scroll and scan posts until we find "Les logiciels libre de l'été 1"
    print("🔍\tScanning posts while scrolling...")

    # Initialize variables for found posts and target post
    found_posts = []
    target_post_found = False
    scroll_count = 0
    max_scrolls = 20
    expanded_count = 0

    while not target_post_found and scroll_count < max_scrolls:
        print(f"🔽\t\tScroll n° {scroll_count + 1}...")

        # Unroll each post to ensure we can read the full content
        # ('... plus' button (in French))
        print("↕️\tExpanding all posts...")
        see_more_spans = driver.find_elements(
            By.XPATH, "//span[contains(text(), '… plus')]"
        )

        for span in see_more_spans:
            try:
                # Scroll the span into view
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", span
                )

                time.sleep(4)

                span.click()
                expanded_count += 1

                time.sleep(4)

            except Exception:
                continue

        print(f"🔢\tExpanded {expanded_count} posts")

        # Wait for all content to load after expansion
        time.sleep(2)

        # Use the selector that targets the complete post content
        # This selector captures the full expanded text with links
        posts = driver.find_elements(
            By.CSS_SELECTOR, "span.break-words.tvm-parent-container"
        )

        print(f"📄\tFound {len(posts)} posts to analyze")

        new_posts_count = 0

        # Analyze each post
        for post in posts:
            try:
                post_text = post.text

                # Check if it's the target post (day 1)
                if "Les Logiciels Libres de l'été, jour 1 :" in post_text:
                    print("🎯\tFound target post: " +
                          "'Les Logiciels Libres de l'été, jour 1 :'")
                    target_post_found = True

                # Apply regex for the posts we're interested in
                main_regex = re.search(
                    r"jour\s*(\d{1,2})\s*[:\-–]?\s*\n*([^:]+)\s*:\s*(.+?)"
                    r"(?:\n|$)",
                    post_text,
                    re.IGNORECASE | re.DOTALL
                )

                # If regex matches, extract the day, title, and description
                if main_regex:
                    day = main_regex.group(1)
                    title = main_regex.group(2).strip()
                    description = main_regex.group(3).strip()

                    # Check if we already know this post (by day)
                    # Then add it if it's new or ignore it if known
                    if day not in known_posts:
                        known_posts.add(day)
                        new_posts_count += 1

                        # Extract all links from the post
                        links = []
                        link_elements = post.find_elements(By.TAG_NAME, "a")
                        for link_el in link_elements:
                            href = link_el.get_attribute('href')
                            if href:
                                links.append(href)

                        found_posts.append({
                            'text': post_text,
                            'day': day,
                            'title': title,
                            'description': description,
                            'links_project': (
                                links[0] if len(links) > 0 else None
                            ),
                            'links_more': (
                                links[1] if len(links) > 1 else None
                            ),
                            'links_support': (
                                links[2] if len(links) > 2 else None
                            )
                        })
                        print(f"⏺️\tFound NEW post: jour {day} - {title}")
                    else:
                        print(f"⏭️\tSkipped known post: jour {day}")

            except Exception as e:
                print(f"⚠️\tError processing post: {e}")
                continue

        print(f"🔎\tFound {new_posts_count} new posts in this scroll")

        if not target_post_found:
            # Scroll down to load more content
            print("🔽\tScrolling down to load more posts...")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
            scroll_count += 1

    if target_post_found:
        print("🏆\tSuccessfully reached target post after " +
              f"{scroll_count} scrolls")
    else:
        print(f"❌\tTarget post not found after {max_scrolls} scrolls")

    # Save all found posts

    print(f"\n📋\tSUMMARY: Found {len(found_posts)} matching posts:")
    if len(found_posts) > 0:
        print("💾\tSaving found posts to CSV file...")
        save_found_posts(found_posts)
    else:
        print("❌\tNo posts to save")


except Exception as e:
    print(f"⚠️\tError during execution: {e}")
    traceback.print_exc()

finally:
    # Close the browser
    driver.quit()

    # Calculate and print execution time
    execution_time = time.time() - start_time
    print(f"⏱️\tExecution time: {execution_time:.2f} seconds")

    # Write the timestamp in a file
    timestamp_path = os.path.join(
        os.path.dirname(script_dir), 'web', 'last_update.txt'
    )
    with open(timestamp_path, "w") as f:
        f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
