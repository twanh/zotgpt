import os

from dotenv import load_dotenv

from flask import Flask, render_template

from .zotero import zotero_bp


def create_app(test_config=None):
    # create and configure the app

    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # Access the ZOTERO_API_KEY from the environment
    zotero_api_key = os.getenv('ZOTERO_API_KEY')
    # if zotero_api_key is None:
    #     raise RuntimeError("ZOTERO_API_KEY is not set in the environment.")

    app.config['ZOTERO_API_KEY'] = zotero_api_key

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(zotero_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
