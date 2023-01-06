#!/usr/bin/env python

# This script converts data sets to the properly expected format.
# converts 2007-01-01 00:00:00 to 18.10.2019 00:00:00.000 GMT+0300
from datetime import datetime, timezone
import csv
import os

input_file = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'new_set.csv')
output_file = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'set.csv')

with open(input_file, 'r') as f_input, open(output_file, 'w', newline='') as f_output:
    csv_input = csv.reader(f_input)
    csv_output = csv.writer(f_output)
    next(csv_input)  # skip header line
    for row in csv_input:
        try:
            # try to parse the date as the original format
            dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # if parsing fails, assume the date is already in the correct format
            print("Row Has Correct Format:", row, "\n")
            csv_output.writerow(row)
            continue
        tz = timezone(timedelta(hours=3))  # create a timezone object for GMT+0300
        dt = dt.replace(tzinfo=tz)  # assign the timezone to the datetime object
        row[0] = dt.strftime('%d.%m.%Y %H:%M:%S.000 GMT+0300')  # assign the revised format
        csv_output.writerow(row)
        print("Successfully Formatted Row:", row, "\n")
    print("Success!")

