def process_item(item):
    new_item = item.copy()
    if new_item['price_usd'] in ['0', '0.0', 'NULL']:
        new_item['price_person'] = 0.0
    else:
        new_item['price_person'] = float(new_item['price_usd']) / (float(new_item['srch_adults_count']) + float(new_item['srch_children_count']))


items = []
# file_items were loaded from csv file
for item in file_items:
    items.append(process_item(item))

# take out those with 0, since we can't do log of that
items = [i for i in items if i['price_person'] != 0.0]

# do log
for item in items:
    item['log_price_person'] = math.log(item['price_person'])

price_logs = [i['log_price_person'] for i in items]
avg = sum(price_logs) / float(len(price_logs))

sq_diffs = []
for price in price_logs:
    diff = price - avg
    sq_diffs.append(diff**2)

variance = sum(sq_diffs) / float(len(sq_diffs))
std_dev = math.sqrt(variance)

# add normalized price person
for item in items:
    item['normalized_price_person'] = (item['log_price_person'] - avg) / std_dev

