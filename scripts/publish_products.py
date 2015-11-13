# -*- coding: utf-8 -*-

import json
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
        resp = requests.post(urlparse.urljoin(host, '/api/post'), data=product)
        if resp.status_code != 200:
            print('Error {} {}: {}'.format(resp.status_code, resp.url, resp.content))
        else:
            print('Successfully posted: {}'.format(resp.content))

if __name__ == '__main__':
    main()