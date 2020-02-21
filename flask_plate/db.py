# -*- coding: utf-8 -*-
import sqlite3
import os
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    app.app_context().push()  # 推送应用上下文环境
    if os.path.exists(current_app.config['DATABASE']):
        return
    g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
    db = g.db
    with current_app.open_resource('flask_plate.sql') as f:
        db.executescript(f.read().decode('utf8'))
        print('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    init_db(app)
