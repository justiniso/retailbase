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
    parser.add_argument('--update', action='store_true', dest='update', help='If set, update products that already exist')

    args = parser.parse_args()
    host = args.host
    update = args.update

    with open(args.products_file) as f:
        data = f.read()

    product_list = json.loads(data)

    for product in product_list:
        time.sleep(0.1)

        # Check to see if the same product exists already, Slug is a unique key in this case

        # Handle legacy older slugs
        resp = requests.get(urlparse.urljoin(host, '/api/post'), params={'slug': product['slug']})

        # Make sure all slugs going in are loweercase
        product['slug'] = product['slug'].lower()
        resp2 = requests.get(urlparse.urljoin(host, '/api/post'), params={'slug': product['slug']})


        if resp.json()['results'] or resp2.json()['results']:
            if update:
                try:
                    id = resp.json()['results'][0]['id']
                except IndexError:
                    id = resp2.json()['results'][0]['id']

                # Delete the product if scheduled for deletion
                if product.get('DELETE') is not None:
                    resp = requests.delete(urlparse.urljoin(host, '/api/post/{}'.format(id)))
                else:
                    # Remove fields that cannot be updated
                    product.pop('slug', None)
                    product.pop('DELETE', None)
                    resp = requests.put(urlparse.urljoin(host, '/api/post/{}'.format(id)), data=product)

                if resp.status_code == 200:
                    print('Successfully updated: {}'.format(id))
                else:
                    print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))
            else:
                print('Skipping product that already exists: {}'.format(product['slug']))
            continue

        resp = requests.post(urlparse.urljoin(host, '/api/post'), data=product)
        if resp.status_code == 200:
            print('Successfully posted: {} / {}'.format(resp.json()['id'], resp.json()['title']))
        else:
            print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))

if __name__ == '__main__':
    main()