from tests.tests_auto.config_tests import *
from models.reserved_running_model import ReservedRunningModel
from models.moto_model import MotoModel
from models.client_model import ClientModel

def startMoto(moto, client_reserve, c):
    # c es el client del contexto
    # client_reserve el cliente de la reserva

    path = "/start"

    params = {
        "client_email": client_reserve.email,
        "moto_id": moto.id
    }

    r = c.post(path, json=params)

    # El post start tiene que funcionar sino no se puede testear nada.
    assert r.status_code == 200

def makeReservation(moto, client_reserve, c):
    # c es el client del contexto
    # client_reserve el cliente de la reserva

    path = "/reserve"

    params = {
        "client_email": client_reserve.email,
        "moto_id": moto.id
    }

    r = c.post(path, json=params)

    # El post reserve tiene que funcionar sino no se puede testear nada.
    assert r.status_code == 201

def getMotoClient():
    moto = MotoModel.query.filter(MotoModel.state == "AVAILABLE").first()
    all_clients = ClientModel.query.all()
    for cliente_sin_reservas in all_clients:
        client_reserve = ReservedRunningModel.query.filter(
            ReservedRunningModel.clientId == cliente_sin_reservas.client_id).first()
        # Devolvemos el primero que NO esté en RR
        if client_reserve is None:
            return moto, cliente_sin_reservas
    # Si llegamos aquí hay que cambiar el add data antes de empezar,
    # sino los tests no pueden funcionar.
    assert False

def test_StopMotoClient_0_GoodRequest(client):
    c = client
    # Hay que hacer una llamada al principio para que funcione.
    c.get("/clients")

    # Cogemos un cliente y una moto que nos valgan.
    moto, client_reserve = getMotoClient()
    # Hacemos la reserva.
    makeReservation(moto, client_reserve, c)
    # We start the moto
    startMoto(moto, client_reserve, c)

    path = "/start"

    params = {
        "client_email": client_reserve.email,
        "moto_id": moto.id
    }

    r = c.put(path, json=params)
    json_data = r.get_json()

    expected_keys = {"message_status", "message"}

    assert set(json_data.keys()) == expected_keys
    assert r.status_code == 200
    assert json_data["message_status"] == "Ok"

def test_StopMotoClient_1_NotStarted_NotFound(client):
    c = client
    # Hay que hacer una llamada al principio para que funcione.
    c.get("/clients")

    # Cogemos un cliente y una moto que nos valgan.
    moto, client_reserve = getMotoClient()
    # Hacemos la reserva.
    makeReservation(moto, client_reserve, c)

    path = "/start"

    params = {
        "client_email": client_reserve.email,
        "moto_id": moto.id
    }

    r = c.put(path, json=params)
    json_data = r.get_json()

    expected_keys = {"message_status", "message"}

    assert set(json_data.keys()) == expected_keys
    assert r.status_code == 404
    assert json_data["message_status"] == "Not Found"

def test_StopMotoClient_2_InventedEmail_NotFound(client):
    c = client
    # Hay que hacer una llamada al principio para que funcione.
    c.get("/clients")

    # Cogemos un cliente y una moto que nos valgan.
    moto, client_reserve = getMotoClient()
    # Hacemos la reserva.
    makeReservation(moto, client_reserve, c)
    # We start the moto
    startMoto(moto, client_reserve, c)

    path = "/start"
    # Invented email
    params = {
        "client_email": "inventadojajejijoju@gmail.com",
        "moto_id": moto.id
    }

    r = c.put(path, json=params)
    json_data = r.get_json()

    expected_keys = {"message_status", "message"}

    assert set(json_data.keys()) == expected_keys
    assert r.status_code == 404
    assert json_data["message_status"] == "Not Found"

def test_StopMotoClient_3_InventedMotoID_NotFound(client):
    c = client
    # Hay que hacer una llamada al principio para que funcione.
    c.get("/clients")

    # Cogemos un cliente y una moto que nos valgan.
    moto, client_reserve = getMotoClient()
    # Hacemos la reserva.
    makeReservation(moto, client_reserve, c)
    # We start the moto
    startMoto(moto, client_reserve, c)

    path = "/start"

    # Invented ID
    params = {
        "client_email": client_reserve.email,
        "moto_id": 1234432239849
    }

    r = c.put(path, json=params)
    json_data = r.get_json()

    expected_keys = {"message_status", "message"}

    assert set(json_data.keys()) == expected_keys
    assert r.status_code == 404
    assert json_data["message_status"] == "Not Found"