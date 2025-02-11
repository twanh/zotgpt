from flask import Blueprint

zotero_bp = Blueprint('zotero', __name__)

@zotero_bp.route('/zotero')
def zotero():
    return 'Welcome to the Zotero page!'
