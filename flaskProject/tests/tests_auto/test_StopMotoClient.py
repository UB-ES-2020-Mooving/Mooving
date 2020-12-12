from tests.tests_auto.config_tests import *

def test_StopMotoClient_0_GoodRequest():
    with app.test_client() as c:
        path = '/clients'
        r = c.get(path)
        json_data = r.get_json()

        assert "clients" in json_data.keys()
        assert r.status_code == 200