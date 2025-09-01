#!/usr/bin/env python3

"""
Script for generating RSS from an existing CSV file
"""

# Import libraries
import time

from populate_rss import build_rss_from_csv

# Execution time calculation
start_time = time.time()

build_rss_from_csv()

# Calculate and print execution time
execution_time = time.time() - start_time
print(f"⏱️\tExecution time: {execution_time:.2f} seconds")
