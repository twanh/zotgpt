from flask import Blueprint, current_app, render_template
from datetime import datetime

from pyzotero.zotero import Zotero

zotero_bp = Blueprint('zotero', __name__)

@zotero_bp.route('/zotero')
def zotero():

    # Initialize Zotero client
    zot = Zotero('6785412', 'user', current_app.config.get('ZOTERO_API_KEY'))

    # Fetch collections
    collections = zot.collections()

    # Organize collections hierarchically
    collections_dict = {}
    for collection in collections:
        data = collection['data']
        collection_key = data['key']
        if not data.get('parentCollection'):
            collections_dict[collection_key] = {'name': data['name'], 'subcollections': [], 'key': collection_key}
        else:
            parent_key = data['parentCollection']
            if parent_key in collections_dict:
                collections_dict[parent_key]['subcollections'].append({'name': data['name'], 'key': collection_key})

    collections_list = [{'name': data['name'], 'subcollections': data['subcollections'], 'key': data['key']} for data in collections_dict.values()]

    return render_template('zotero/index.html', collections=collections_list)

@zotero_bp.route('/zotero/collection/<collection_key>')
def collection_items(collection_key):
    # Initialize Zotero client
    zot = Zotero('6785412', 'user', current_app.config.get('ZOTERO_API_KEY'))

    # Fetch items in the specified collection
    items = zot.collection_items(collection_key)


    # Extract relevant data from items
    items_list = [
        {
            'title': item['data'].get('title', 'Untitled'),
            'raw_json': item['data'],
            'formatted_date': datetime.strptime(item['data']['dateAdded'], '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y %I:%M %p')
        }
        for item in items if item['data'].get('itemType') not in ['attachment', 'note']
    ]

    return render_template('zotero/collection_items.html', items=items_list)

@zotero_bp.route('/zotero/item/<item_key>')
def view_item(item_key):
    # Initialize Zotero client
    zot = Zotero('6785412', 'user', current_app.config.get('ZOTERO_API_KEY'))

    # Fetch the item details
    item = zot.item(item_key)
    item_data = item['data']

    # Determine if the content is text or PDF
    content_type = 'text' if 'note' in item_data.get('itemType', '') else 'pdf'

    return render_template('zotero/view_item.html', item=item_data, content_type=content_type)
