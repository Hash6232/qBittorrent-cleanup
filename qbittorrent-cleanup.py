#!/usr/bin/python

import requests
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-b','--baseurl', help='Override url to qBittorrent. Defaults to http://localhost:8080/')
args=parser.parse_args()

baseurl = 'http://localhost:8080/'

if args.baseurl:
    baseurl = args.baseurl

url = 'api/v2/torrents/info?filter=completed'

def has_tag(string, word):
    return any(word in s for s in string.split())

try:
    response = requests.get(baseurl+url)
    response.raise_for_status()
    data = response.json()

    if len(data) == 0:
        exit(0)

    for torrent in data:
        if has_tag(torrent['tags'], 'flexget') and torrent['ratio'] >= 2:
            form_data = { 'hashes': str(torrent['hash']), 'deleteFiles':'false' }

        url = 'api/v2/torrents/delete'

        try:
            response = requests.post(baseurl+url,data=form_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
            continue

    exit(0)
except requests.exceptions.RequestException as err:
    print(err)
    exit(1)
