import csv
import math
import sys


# add new attributes
def process_item(item):
    new_item = item.copy()

    if new_item['price_usd'] in ['0', '0.0', 'NULL']:
        new_item['price_diff'] = 0.0
    else:
        new_item['price_diff'] = math.log(float(new_item['price_usd'])) - float(new_item['prop_log_historical_price'])

    if new_item['price_usd'] in ['0', '0.0', 'NULL']:
        new_item['price_person'] = 0.0
    else:
        new_item['price_person'] = float(new_item['price_usd']) / (float(new_item['srch_adults_count']) + float(new_item['srch_children_count']))

    if new_item['srch_length_of_stay'] in ['0', '0.0', 'NULL']:
        new_item['price_night'] = float(new_item['price_usd'])
    else:
        per_night = float(new_item['price_usd']) / float(new_item['srch_length_of_stay'])
        new_item['price_night'] = per_night if per_night > 20 else float(new_item['price_usd'])

    if new_item['visitor_hist_starrating'] in ['0', '0.0', 'NULL']:
        new_item['star_diff'] = 0.0
    else:
        new_item['star_diff'] = float(new_item['prop_starrating']) - float(new_item['visitor_hist_starrating'])

    if new_item['visitor_hist_adr_usd'] in ['0', '0.0', 'NULL']:
        new_item['pay_diff'] = 0.0
    else:
        new_item['pay_diff'] = float(new_item['price_night']) - float(new_item['visitor_hist_adr_usd'])

    if new_item['prop_location_score1'] in ['0', '0.0', 'NULL']:
        new_item['loc_desire'] = 0
    else:
        new_item['loc_desire'] = float(new_item['prop_location_score1'])
    if new_item['prop_location_score2'] in ['0', '0.0', 'NULL']:
        new_item['loc_desire'] += 0
    else:
        new_item['loc_desire'] += 3 * float(new_item['prop_location_score2'])

    new_item['no_kids'] = 1 if float(new_item['srch_children_count']) > 0 else 0
    new_item['couple'] = 1 if float(new_item['srch_adults_count']) and new_item['no_kids'] else 0
    new_item['price_down'] = 1 if new_item['price_diff'] < 0 else 0
    new_item['same_country'] = 1 if new_item['visitor_location_country_id'] == new_item['prop_country_id'] else 0


    return new_item


with open(sys.argv[1]) as fin, open(sys.argv[2], 'w') as fout:
    dr = csv.DictReader(fin)

    new_fields = [
        'price_diff',
        'price_person',
        'star_diff',
        'pay_diff',
        'price_night',
        'loc_desire',
        'no_kids',
        'couple',
        'price_down',
        'same_country',
    ]
    dw = csv.DictWriter(fout, dr.fieldnames + new_fields)
    dw.writeheader()

    for item in dr:
        processed_item = process_item(item)
        dw.writerow(processed_item)


