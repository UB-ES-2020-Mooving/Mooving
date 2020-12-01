from tests.tests_auto.config_tests import *


def test_moto_reserve():

    with app.test_client() as c:

        # Path POST moto reserve (client_email = juanita@gmail.com / moto_id = 1)
        r = c.post('/reserve', json={
            "client_id": "juanita@gmail.com",
            "moto_id": "2"
            })
        json_data_post = r.get_json()

        # Comprobamos si el estatus code es 201
        assert r.status_code == 201

        # Comprobamos que el encabezado del json sea el adecuado
        list_keys = ['message', 'remaining_time']
        assert "reserved_moto" in json_data_post.keys()


        # Path GET moto reserve (client_email = juanita@gmail.com)
        path = '/reserve/juanita@gmail.com'

        r = c.get(path)

        json_data_get = r.get_json()

        # Comprobamos si el estatus code es 201
        assert r.status_code == 201

        # Comprobamos que el encabezado del json sea el adecuado
        assert "reserved_moto" in json_data_get.keys()

        # Capturamos el cuerpo del json
        json_body = json_data_get["reserved_moto"]

        # Comprobamos los valores del Json
        list_keys = ['id', 'matricula', 'model_generic', 'km_restantes', 'address', 'last_coordinate_latitude', 'last_coordinate_longitude', 'address']
        assert list(json_body.keys()) == list_keys
