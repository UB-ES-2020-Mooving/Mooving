import os
import tempfile

import pytest

from data_tests import add_data, clear_data
from app import app
from flask import request, jsonify
from db import db

# No es client de cliente de la aplicación sinó en el sentido
# de cliente en el contexto de APIs, Responses etc...

'''
File containing set-ups for running tests
Right now, it's not necessary to import db,
but it goes 10s faster (magic?)
'''


@pytest.fixture
def client():
    '''
    Create an app instance for testing.
    With a brand new database each time, the same as always, data.db, sql3ite
    
    TO USE IT: your test must have 'client' as a parameter
    you can use client as you used c before
    you can even do c = client so previous code work
    '''
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            clear_data(db)
            add_data(db)
        yield client
