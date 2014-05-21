import csv
import math
import sys
import time
from operator import itemgetter
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.data_mining_db
collection = db.big_training_set


def compute_score(prop_id):
    docs = collection.find({'prop_id': prop_id}, fields=['position', 'booking_bool', 'click_bool'], exhaust=True)
    score = 0

    positions = []
    bookings = 0
    clicks = 0
    for doc in docs:
        positions.append(doc['position'])
        bookings += doc['booking_bool']
        clicks += doc['click_bool']

    for position in positions:
        score += 5 + (10.0 / position) - math.log(position, 2)

    score += bookings * 45
    score += clicks * 15

    return score

cached_scores = {}
def process_chunk(chunk):
    if len(chunk) == 0:
        return

    processed_chunk = []
    for srch_id, prop_id in chunk:
        if prop_id in cached_scores:
            score = cached_scores[prop_id]
        else:
            score = compute_score(prop_id)
            cached_scores[prop_id] = score
        # (srch_id, prop_id, score)
        processed_chunk.append((srch_id, prop_id, score))

    # order by score
    processed_chunk.sort(key=itemgetter(2), reverse=True)
    return processed_chunk


results = open(sys.argv[2], 'w')
results.write('SearchId,PropertyId\n')

### TIMING STUFF
count = 0
since = time.time()
TOTAL_ROWS = 6622630

# read chunks of search queries
current_id = None
current_chunk = []
with open(sys.argv[1]) as f:
    next(f)
    for line in f:
        words = line.split(',')
        srch_id = int(words[0])
        prop_id = int(words[7])
        if srch_id != current_id:
            # process the current chunk
            processed_chunk = process_chunk(current_chunk)

            if processed_chunk:
                for i_srch_id, i_prop_id, _ in processed_chunk:
                    results.write('%d,%d\n' % (i_srch_id, i_prop_id))

                #### TIMING STUFF
                count += len(processed_chunk)
                if count >= 100000:
                    t = time.time()
                    s = t - since
                    since = t
                    per_hour = 3600.0 / s * count
                    print("Did 100000 rows in %.2f seconds. That is %d rows per hour. Got %d rows left, so %.2f hours." % (s, per_hour, TOTAL_ROWS - count, (TOTAL_ROWS - count) / per_hour))
                    TOTAL_ROWS -= count
                    count = 0

            # start working on the next chunk
            current_id = srch_id
            current_chunk = []

        current_chunk.append((srch_id, prop_id))

# do last chunk
processed_chunk = process_chunk(current_chunk)
if processed_chunk:
    for i_srch_id, i_prop_id, _ in processed_chunk:
        results.write('%d,%d\n' % (i_srch_id, i_prop_id))


results.close()

