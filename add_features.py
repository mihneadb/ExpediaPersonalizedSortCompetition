import csv
import math
import sys


# add new attributes
def process_item(item):
    new_item = item.copy()

    if new_item['price_usd'] in ['0', '0.0']:
        new_item['price_diff'] = 0.0
    else:
        new_item['price_diff'] = math.log(float(new_item['price_usd'])) - float(new_item['prop_log_historical_price'])

    if new_item['price_usd'] in ['0', '0.0']:
        new_item['price_person'] = 0.0
    else:
        new_item['price_person'] = float(new_item['price_usd']) / (float(new_item['srch_adults_count']) + float(new_item['srch_children_count']))

    return new_item


with open(sys.argv[1]) as fin, open(sys.argv[2], 'w') as fout:
    dr = csv.DictReader(fin)

    new_fields = [
        'price_diff',
        'price_person',
    ]
    dw = csv.DictWriter(fout, dr.fieldnames + new_fields)
    dw.writeheader()

    for item in dr:
        processed_item = process_item(item)
        dw.writerow(processed_item)


