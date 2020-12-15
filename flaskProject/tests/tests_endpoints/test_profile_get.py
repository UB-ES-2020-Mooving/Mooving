from tests.tests_endpoints.config_tests import *

def test_profile_get(client):
    get_response = client.get("/profile/juanita@gmail.com")
    get_keys = get_response.get_json().keys()
    assert "client_profile" in get_keys
    json_interior_fields = (get_response.get_json()['client_profile']).keys()
    assert "nombre" in json_interior_fields
    assert "iban" in json_interior_fields
    assert "dni_nie" in json_interior_fields
    assert "email" in json_interior_fields