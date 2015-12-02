# -*- coding: utf-8 -*-
"""
Usage:

    python publish_products.py -p data/products001.json --host http://127.0.0.1:5000
"""

import json
import time
import urlparse
from argparse import ArgumentParser

import requests


def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', dest='products_file')
    parser.add_argument('--host', dest='host')
    parser.add_argument('--update', action='store_true', dest='update', help='If set, update categories that already exist')

    args = parser.parse_args()
    host = args.host
    update = args.update

    with open(args.products_file) as f:
        data = f.read()

    category_list = json.loads(data)

    for category in category_list:
        time.sleep(0.1)

        # Check to see if the same product exists already, Slug is a unique key in this case

        # Handle legacy older slugs
        resp = requests.get(urlparse.urljoin(host, '/api/category'), params={'slug': category['slug']})

        # Make sure all slugs going in are lowercase
        category['slug'] = category['slug'].lower()
        resp2 = requests.get(urlparse.urljoin(host, '/api/category'), params={'slug': category['slug']})

        if resp.json()['results'] or resp2.json()['results']:
            if update:
                id = resp.json()['results'][0]['id']
                resp = requests.put(urlparse.urljoin(host, '/api/category/{}'.format(id)), data=category)
                if resp.status_code == 200:
                    print('Successfully updated: {}'.format(id))
                else:
                    print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))
            else:
                print('Skipping product that already exists: {}'.format(category['slug']))
            continue

        resp = requests.post(urlparse.urljoin(host, '/api/category'), data=category)
        if resp.status_code == 200:
            print('Successfully posted: {} / {}'.format(resp.json()['id'], resp.json()['title']))
        else:
            print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))

if __name__ == '__main__':
    main()