import pprint
import os

from pyzotero import zotero

# Load API key from ENV
api_key = os.environ.get('ZOTERO_API_KEY')

zot = zotero.Zotero('6785412', 'user', api_key)

collections = zot.all_collections()

for collection in collections:
    print(collection['data']['name'], collection['data']['key'])


collection_key = 'L6MRARQT'

items = zot.collection_items(collection_key)

for item in items:
    pprint.pprint(item)
