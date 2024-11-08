import csv
import json
import requests

import os
from os.path import join

def regenerate_collection_list(collection_csv):
    coll_items = list()

    with open(collection_csv, 'r', newline='', encoding='utf-8') as f:
        data = csv.DictReader(f)

        for row in data:
            row_dict = dict()
            for field in data.fieldnames:
                row_dict[field] = row[field]
            coll_items.append(row_dict)

        return coll_items

collection_csv = os.path.join('.','assignment-1','collection_list.csv')

collection_list = regenerate_collection_list(collection_csv)
## print(collection_list[0])

baseurl = 'https://www.loc.gov'
parameters = {
    'fo' : 'json'
}

error_count = 0
item_count = 0
file_count = 0


data_directory = 'assignment-1'
item_metadata_directory = 'item-metadata'
file_prefix = 'im_'
json_suffix = '.json'

for item in collection_list:
        item_id = item['link']
        file_id = item['link'].split('/')[2]
        item_metadata = requests.get(baseurl + item_id, params=parameters)
        print('requested', item_metadata.url,item_metadata.status_code)
        if item_metadata.status_code != 200:
            print('error for requested',item_metadata.url,item_metadata.status_code)
            error_count += 1
            continue
        try:
            item_metadata.json()
        except:
            error_count += 1
            print('no json found')
            continue
        fout = os.path.join('.',data_directory,item_metadata_directory,
                            str(file_prefix + file_id + json_suffix))
        with open(fout, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(item_metadata.json()['item']))
            file_count += 1
            print('wrote', fout)
        item_count += 1

print('---LOG---')
print('items requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)