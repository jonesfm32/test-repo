import csv
import json
import requests

import os
from os.path import join
import glob

project_dir = 'assignment-1'
metadata_dir = 'item-metadata'
files_dir = "item-files"

metadata_search = os.path.join('.',project_dir,metadata_dir)
#print(metadata_search)
metadata_file_list = glob.glob(metadata_search + '/*.json')
#print(metadata_file_list)

img_urls = list()
count = 0

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        img_url_no = len(metadata['image_url'])
        img_url = metadata['image_url'][-1]
        img_urls.append(img_url)
        count += 1

print(f'Identified { str(count) } image URLs')

collection_list_with_imgs = list()

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as item_info:
        item_metadata = json.load(item_info)
        item_metadata_dict = dict()
        item_metadata_dict['item_uri'] = item_metadata['id']
        try:
            item_metadata_dict['lccn'] = item_metadata['library_of_congress_control_number']
        except:
            item_metadata_dict['lccn'] = None
        item_metadata_dict['title'] = item_metadata['title']
        item_metadata_dict['image_url_large'] = item_metadata['image_url'][-1]

        collection_list_with_imgs.append(item_metadata_dict)
print(collection_list_with_imgs[0])

item_count = 0
error_count = 0
file_count = 0

img_file_prefix = 'img_'

for item in collection_list_with_imgs:
        img_url = item['image_url_large']
        img_id = item['item_uri'].split('/')[-2]
        print('request',img_url)
        item_count += 1

        # if found, save image
        r = requests.get(img_url)
        if r.status_code == 200:
            img_out = os.path.join('.',project_dir,files_dir,str(img_file_prefix + img_id + '.jpg'))
            with open(img_out, 'wb') as file:
                file.write(r.content)
                print('Saved',img_out)
                file_count += 1


print('---LOG---')
print('files requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)