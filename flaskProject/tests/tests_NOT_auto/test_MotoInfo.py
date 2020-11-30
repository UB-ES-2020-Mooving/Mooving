from models.moto_model import MotoModel
#import requests


def test_street_variable():
    """
    GIVEN a MotoModel model
    WHEN a new MotoModel is created
    THEN check the address field is defined correctly
    """
    new_moto = MotoModel(
        state="ACTIVE",
        matricula="1234-MMM",
        date_estreno="24/11/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4434,
        last_coordinate_longitude=23.4433,
        km_restantes=120.0,
        km_totales=0.0,
        date_last_check="24/11/2020",
        km_last_check=0.0)

    assert new_moto.address == "Al Kufrah, Libia"


def test_jsonMotoPageClient():
    """
    GIVEN a resource ClientMoto
    WHEN a GET request (for a concrete moto's info) is called
    THEN check the json fields are returned correctly, has all required fields.
    """

    #OBS: Run pytest in the 2nd terminal while your 1st terminal is executing the flask app.
    url = 'http://127.0.0.1:5000'  # The root url of the flask app
    r = requests.get(url + '/clientMoto/1')  # Assumses that it has a moto with id 1 in database.
    assert r.status_code == 200

    data = r.json()
    assert 'client_moto' in data.keys()
    json_fields = data['client_moto'].keys()
    assert 'id' in json_fields
    assert 'matricula' in json_fields
    assert 'model_generic' in json_fields
    assert 'km_restantes' in json_fields
    assert 'address' in json_fields
    assert 'distance' in json_fields
