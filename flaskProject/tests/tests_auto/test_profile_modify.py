from tests.tests_auto.config_tests import *
from models.client_model import ClientModel

def test_profile_modify_correct(client):

    c = client
    c.get("/clients")

    # Cogemos un cliente random de la base de datos.
    client_old = ClientModel.query.filter(ClientModel.client_id == 1).first()

    # Nos inventamos datos
    new_email = "inventado@inventado.com"
    new_dni_nie = "000000000000"
    new_name = "Inventado"
    new_iban = "0000000000000000000000"

    # Nos aseguramos de que no exista ese email en la base de datos
    assert ClientModel.find_by_email(new_email) is None

    # Nos aseguramos de que no exista ese dni en la base de datos
    assert ClientModel.find_by_dni(new_dni_nie) is None

    # Hacemos el put con datos inventados
    path = '/profile/' + client_old.email
    params = {
        'name': new_name,
        'iban': new_iban,
        'dni_nie': new_dni_nie,
        'email': new_email
    }
    r = c.put(path, json=params)

    assert r.status_code == 200

    # Antes de nada comprobamos si realmente se han modificado el email o el dni
    assert ClientModel.find_by_email(new_email) is not None

    assert ClientModel.find_by_dni(new_dni_nie) is not None

    # Ahora comprobaremos los otros datos
    new_client = ClientModel.find_by_email(new_email)

    assert new_client.nombre == new_name
    assert new_client.iban == new_iban
    assert new_client.dni_nie == new_dni_nie
    assert new_client.email == new_email


def test_profile_modify_error1(client): # Cuando no se encuentra el cliente de la url
    c = client

    # Hacemos el put con datos inventados
    path = '/profile/inventado@gmail.com'
    params = {
        'name': "new_name",
        'iban': 1111,
        'dni_nie': 111,
        'email': "gmail"
    }
    r = c.put(path, json=params)

    assert r.status_code == 404


def test_profile_modify_error2(client): # El cliente introduce un nuevo email ya en uso
    c = client
    c.get("/clients")

    # Cogemos un cliente random de la base de datos.
    client_old = ClientModel.query.filter(ClientModel.client_id == 1).first()

    # Hacemos el put con datos inventados menos el email
    path = '/profile/camila@gmail.com'
    params = {
        'name': "new_name",
        'iban': 1111,
        'dni_nie': 111,
        'email': client_old.email
    }
    r = c.put(path, json=params)

    assert r.status_code == 405


def test_profile_modify_error3(client):  # El cliente introduce un nuevo dni_nie ya en uso
    c = client
    c.get("/clients")

    # Cogemos un cliente random de la base de datos.
    client_old = ClientModel.query.filter(ClientModel.client_id == 1).first()

    # Hacemos el put con datos inventados menos el dni
    path = '/profile/camila@gmail.com'
    params = {
        'name': "new_name",
        'iban': 1111,
        'dni_nie': client_old.dni_nie,
        'email': "gmail"
    }
    r = c.put(path, json=params)

    assert r.status_code == 406




