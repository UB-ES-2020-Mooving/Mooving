from tests.tests_endpoints.config_tests import *

# Es el mismo que test_clients_post.py que el anterior, pero solo para que veas que se
# ejecutan ambos si ejecutas pytest, aunque puedes ejecutarlos por separado
# si haces uso de los botones de play que salen a la izquierda de los
# nombres.


def test_ejemplo2(client):
    c = client
    path = '/clients'
    r = c.open(path)
    json_data = r.get_json()

    assert "clients" in json_data.keys()
    assert r.status_code == 200


def test_prueba2(client):
    c = client
    path = '/clients'
    r = c.get(path)
    json_data = r.get_json()

    assert "clients" in json_data.keys()
    assert r.status_code == 200
    # assert len(json_data["clients"]) == 5

    path = '/client'
    params = {
        "nombre": "Pepito",
        "email": "pepito_prueba@gmail.com",
        "iban": "23452345234523",
        "dni_nie": "88783330D",
        "password": "cacatua"
    }
    r = c.post(path, json=params)
    assert r.status_code == 201