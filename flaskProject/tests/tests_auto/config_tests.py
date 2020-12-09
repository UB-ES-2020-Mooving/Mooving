import os
import tempfile

import pytest

from add_data_tests import init_db_tests
from app import app
from flask import request, jsonify

# No es client de cliente de la aplicación sinó en el sentido
# de cliente en el contexto de APIs, Responses etc...


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():

            init_db_tests()
            yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
