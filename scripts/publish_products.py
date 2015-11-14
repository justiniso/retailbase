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
    parser.add_argument('-p', '--products-file', dest='products_file')
    parser.add_argument('--host', dest='host')

    args = parser.parse_args()
    host = args.host

    with open(args.products_file) as f:
        data = f.read()

    product_list = json.loads(data)

    for product in product_list:
        # Check to see if the same product exists already
        slug = product.get('slug')

        if not slug:
            print 'Skipping product with not slug: {}'.format(product)
            continue

        resp = requests.get(urlparse.urljoin(host, '/api/post'), params={'slug': product['slug']})

        if resp.json()['results']:
            print('Skipping product that already exists: {}'.format(product['slug']))
            continue

        resp = requests.post(urlparse.urljoin(host, '/api/post'), data=product)
        if resp.status_code != 200:
            print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))
        else:
            print('Successfully posted: {} / {}'.format(resp.json()['id'], resp.json()['title']))

        time.sleep(0.3)

if __name__ == '__main__':
    main()