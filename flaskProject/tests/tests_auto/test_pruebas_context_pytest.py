from tests.tests_auto.config_tests import *

def test_get_list(client):
    with client as c:
        path = "/clients"
        r = c.get(path)
        json_data = r.get_json()

        assert len(json_data("clients")) == 4
