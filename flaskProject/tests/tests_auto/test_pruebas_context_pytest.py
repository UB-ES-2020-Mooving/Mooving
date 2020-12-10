from tests.tests_auto.config_tests import *

def test_get_list(client):
    c = client
    path = "/clients"
    r = c.get(path)
    json_data = r.get_json()

    assert 4 == 5
