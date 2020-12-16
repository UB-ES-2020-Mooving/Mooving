from tests.tests_endpoints.config_tests import *

def test_moto_Put_ModifyMoto():
    """
       Test  "/moto/<int:id>" endpoint with PUT call:
       - successful call
       - data correctly updated
    """
    with app.test_client() as c:
        path = '/moto/1'
        params = {
            'matricula': '1234-AAA',
            'km_restantes': 50.0,
            'state': "AVAILABLE"
        }
        r = c.put(path, json=params)
        assert r.status_code == 200


        path = '/mechanicMoto/1'
        r = c.get(path)
        assert r.status_code == 200
        json_data = r.get_json()
        assert json_data['mechanic_moto']['matricula'] == "1234-AAA"
        assert json_data['mechanic_moto']['state'] == "AVAILABLE"
        assert json_data['mechanic_moto']['km_restantes'] == 50.0
        assert json_data['mechanic_moto']['km_since_last_check'] == 0.0
        assert json_data['mechanic_moto']['time_since_last_check'] == 0


def test_moto_Put_ModifyMotoCaseNotFoundMoto():
    """
        Test  "/moto/<int:id>" endpoint with PUT call:
           - call with an unexisting moto id return Not found 404
    """
    with app.test_client() as c:
        path = '/moto/1000'
        params = {
            'matricula': '1234-AAA',
            'km_restantes': 50.0,
            'state': "AVAILABLE"
        }
        r = c.put(path, json=params)
        assert r.status_code == 404


def test_moto_Put_ModifyMotoCaseError():
    """
        Test  "/moto/<int:id>" endpoint with PUT call:
           - call with not suitable data, raise exception, return 500
    """
    with app.test_client() as c:
        path = '/moto/1'
        params = {
            'matricula': '4321-AAA',
            'km_restantes': 50,
            'state': 100
        }
        r = c.put(path, json=params)
        assert r.status_code == 500


def test_moto_Put_ModifyMotoMatriculaError():
    """
        Test  "/moto/<int:id>" endpoint with PUT call:
           - call with license plate incorrect (same as another motorbike), return 409
    """
    with app.test_client() as c:
        path = '/moto/1'
        params = {
            'matricula': '1234-AAA',
            'km_restantes': 150.0,
            'state': "AVAILABLE"
        }
        r = c.put(path, json=params)
        assert r.status_code == 200

        path = '/moto/1'
        params = {
            'matricula': '2222-MMM',
            'km_restantes': 50.0,
            'state': "AVAILABLE"
        }
        r = c.put(path, json=params)
        assert r.status_code == 409


def test_moto_Put_ModifyMotoBatteryStateError():
    """
        Test  "/moto/<int:id>" endpoint with PUT call:
           - call with battery and state fields inconsistent,, return 400
    """
    with app.test_client() as c:
        path = '/moto/1'
        params = {
            'matricula': '1234-AAA',
            'km_restantes': 5.0,
            'state': "AVAILABLE"
        }
        r = c.put(path, json=params)
        assert r.status_code == 400

        path = '/moto/1'
        params = {
            'matricula': '1234-AAA',
            'km_restantes': 50.0,
            'state': "LOW_BATTERY_FUEL"
        }
        r = c.put(path, json=params)
        assert r.status_code == 400




