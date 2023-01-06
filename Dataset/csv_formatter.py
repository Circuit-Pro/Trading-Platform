#!/usr/bin/env python

# CSV Formatter v1.0 - JPR

# This script takes all '.csv' data set's, merges, and converts data sets to
# the properly expected format and merges them into a single output file.
# Converts 2021-09-29 03:05:00	1.26895	1.26919	1.26885	1.26896	241
# to 18.10.2019 00:00:00.000 GMT+0300,108.706,108.724,108.388,108.433,148743.36

import csv
import os
import glob
from tqdm import tqdm
from datetime import datetime, timedelta, timezone

# Set input and output directories
input_dir = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'Merge')
output_file = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'set.csv')

# Get a list of all CSV files in the input directory
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# Open the output file for writing
with open(output_file, 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)

    # Iterate through all CSV files in the input directory
    for input_file in tqdm(csv_files, unit="file"):
        with open(input_file, 'r') as f_input:
            csv_input = csv.reader(f_input, delimiter='\t')  # use '\t' as the delimiter

            # Write a newline between the end of one file and the beginning of another
            if f_output.tell() > 0:
                f_output.write('\n')

            # Iterate through all rows in the CSV file
            for i, row in enumerate(csv_input):
                date_time = row[0]  # extract the date and time value
                try:
                    # try to parse the date as the original format
                    dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # if parsing fails, assume the date is already in the correct format
                    csv_output.writerow(row)
                    continue
                tz = timezone(timedelta(hours=3))  # create a timezone object for GMT+0300
                dt = dt.replace(tzinfo=tz)  # assign the timezone to the datetime object
                date_time = dt.strftime('%d.%m.%Y %H:%M:%S.000 GMT+0300')  # assign the revised format
                row[0] = date_time  # update the date and time value in the row
                csv_output.writerow(row)  # write the row to the output file
    print("Success!")