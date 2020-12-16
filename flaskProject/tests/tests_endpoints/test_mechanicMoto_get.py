from tests.tests_endpoints.config_tests import *

def test_jsonMotoPageMechanic():
    with app.test_client() as c:
        # Aquí ponemos el path del endpoint
        path = '/mechanicMoto/1' # Assumses that it has a moto with id 1 in database.
        # Aquí llamamos al enpoint en cuestión con el método y el path
        r = c.get(path)
        assert r.status_code == 200
        data = r.get_json()
        assert 'mechanic_moto' in data.keys()
        json_fields = data['mechanic_moto'].keys()
        assert 'id' in json_fields
        assert 'matricula' in json_fields
        assert 'state' in json_fields
        assert 'type' in json_fields
        assert 'km_total' in json_fields
        assert 'time_total' in json_fields
        assert 'time_since_last_check' in json_fields
        assert 'km_since_last_check' in json_fields
        assert 'km_restantes' in json_fields
        assert 'address' in json_fields
        assert 'distance' in json_fields