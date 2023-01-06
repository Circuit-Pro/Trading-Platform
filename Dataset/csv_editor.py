#!/usr/bin/env python

# This script converts data sets to the properly expected format.
# converts 2021-09-29 03:05:00	1.26895	1.26919	1.26885	1.26896	241
# to 18.10.2019 00:00:00.000 GMT+0300,108.706,108.724,108.388,108.433,148743.36

import os
import csv
import pandas as pd
from datetime import datetime, timedelta, timezone

line = 0
input_file = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'new_set.csv')
output_file = os.path.join(os.getcwd(), 'Trading-Platform', 'Dataset', 'set.csv')

with open(input_file, 'r') as f_input, open(output_file, 'w', newline='') as f_output:
    csv_input = csv.reader(f_input, delimiter='\t')  # use '\t' as the delimiter
    csv_output = csv.writer(f_output)
    f_input.seek(0)
    total = len(pd.read_csv(f_input))
    for row in csv_input:
        line += 1
        date_time = row[0]  # extract the date and time value
        try:
            # try to parse the date as the original format
            dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # if parsing fails, assume the date is already in the correct format
            csv_output.writerow(row)
            print("Row Has Correct Format:", row, "Current : Total", line,":", len(csv_input), "\n")
            continue
        tz = timezone(timedelta(hours=3))  # create a timezone object for GMT+0300
        dt = dt.replace(tzinfo=tz)  # assign the timezone to the datetime object
        date_time = dt.strftime('%d.%m.%Y %H:%M:%S.000 GMT+0300')  # assign the revised format
        row[0] = date_time  # update the date and time value in the row
        csv_output.writerow(row)  # write the row to the output file
        print("Successfully Formatted Row:", row, "Current : Total", line,":", total, "\n")
    print("Success!")