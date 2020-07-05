# -*- coding: utf-8 -*-
import os
from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, static_folder='static', static_url_path='')
    database_path = os.path.join(app.root_path, '..', 'database')
    app.config.from_mapping(
        DEBUG=False,
        ENV='development',
        SECRET_KEY='dev',
        DATABASE=os.path.join(database_path, 'flask_img.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(database_path)
    except OSError:
        pass

    from . import main
    app.register_blueprint(main.bp)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        return app.send_static_file('index.html')
    app.add_url_rule('/', endpoint='index')

    return app
