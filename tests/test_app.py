# -*- coding: utf-8 -*-
import os, sys

import pytest
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
from flask_img import create_app

def test_app():
    app = create_app()
    print('create_app success')
