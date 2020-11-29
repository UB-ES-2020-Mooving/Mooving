import requests

def test_jsonMotoPageMechanic():
    """
    GIVEN a resource MechanicMoto
    WHEN a GET request (for a concrete moto's info) is called
    THEN check the json fields are returned correctly, has all required fields.
    """

    #OBS: Run pytest in the 2nd terminal while your 1st terminal is executing the flask app.
    url = 'http://127.0.0.1:5000'  # The root url of the flask app
    r = requests.get(url + '/mechanicMoto/1')  # Assumses that it has a moto with id 1 in database.
    assert r.status_code == 200

    data = r.json()
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