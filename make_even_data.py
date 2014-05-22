# gets in csv file with all data, outputs csv file with given number of positive
# and negative data
# negative = no book and no click

import csv
import sys
import time

FILE_ROWS = 9917531
TOTAL_ROWS = 2 * 400000
count = 0
since = time.time()

def process_chunk(chunk):
    good = [l for l in chunk if int(l['click_bool']) or int(l['booking_bool'])]
    bad = [l for l in chunk if not int(l['click_bool']) and not int(l['booking_bool'])][:len(good)]
    res = good + bad
    return res

filtered = []

current_id = None
current_chunk = []
with open(sys.argv[1]) as f:
    dr = csv.DictReader(f)
    for line in dr:
        srch_id = line['srch_id']
        if srch_id != current_id:
            if current_chunk:
                r = process_chunk(current_chunk)
                filtered.append(r)
                TOTAL_ROWS -= len(r)

                if TOTAL_ROWS < 0:
                    break

                count += len(current_chunk)
                if count > 100000:
                    t = time.time()
                    s = t - since
                    since = t
                    per_hour = 3600.0 / s * count
                    print("Did 100000 rows in %.2f seconds. That is %d rows per hour. Got %d rows left, so %.2f minutes." % (s, per_hour, FILE_ROWS - count, (FILE_ROWS - count) / per_hour * 60))
                    FILE_ROWS -= count
                    count = 0

            # start working on the next chunk
            current_id = srch_id
            current_chunk = []

        current_chunk.append(line)

if TOTAL_ROWS > 0:
    # need the last chunk too?
    r = process_chunk(current_chunk)
    filtered.append(r)
    TOTAL_ROWS -= len(r)


print "Done reading."


# write them in csv
with open('even_data.csv', 'w') as f:
    wr = csv.DictWriter(f, dr.fieldnames)
    wr.writeheader()
    for chunk in filtered:
        wr.writerows(chunk)

