from tests.tests_auto.config_tests import *

def test_ejemplo():
    with app.test_client() as c:
        # Aquí ponemos el path del endpoint
        path = '/clientMoto/1'
        params = {
            "client_coordinate_latitude": 41.387677,
            "client_coordinate_longitude": 2.169320,
        }
        # Aquí llamamos al enpoint en cuestión con el método y el path
        r = c.get(path, json=params)
        assert r.status_code == 200
        json_data = r.get_json()
        assert 'client_moto' in json_data.keys()
        json_fields = json_data['client_moto'].keys()
        assert 'id' in json_fields
        assert 'matricula' in json_fields
        assert 'model_generic' in json_fields
        assert 'km_restantes' in json_fields
        assert 'address' in json_fields
        assert 'distance' in json_fields
