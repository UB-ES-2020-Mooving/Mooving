from tests.tests_auto.config_tests import *
from models.client_model import ClientModel

# Comprobacion del caso basico de delete client donde
def test_client_delete_basic():

    with app.test_client() as c:

        # Primero cogemos todos los clientes para comprobar su numero
        path = '/clients'
        r = c.get(path)
        json_data = r.get_json()

        # Comprobamos si el estatus code es 200
        assert (r.status_code == 200)

        # Suponiendo que funciona all sobre get clients, no hago mas compobaciones de get clients
        len_clients = len(json_data["clients"])

        ################################################################################################################

        # Creamos un cliente nuevo para que no haya conflictos con las reservas y starts
        r = c.post('/client', json={
            "nombre": "Test test test",
            "email": "test_delete_client222@gmail.com",
            "iban": "1234567890",
            "dni_nie": "12312222312T",
            "password": "123456"
        })
        json_data = r.get_json()

        # Comprobamos si el estatus code es 200
        assert (r.status_code == 201)

        ################################################################################################################

        # Luego borramos el cliente creado anteriormente
        r = c.delete('/client/test_delete_client222@gmail.com', json={
            "password": "123456"
            })
        json_data_delete = r.get_json()

        # Comprobamos si el estatus code es 201
        assert r.status_code == 200

        ################################################################################################################

        # Volvemos a coger todos los clientes para comprobar los cambios que se han producido
        path = '/clients'
        r = c.get(path)
        json_data_get = r.get_json()

        # Comprobamos si el estatus code es 200
        assert (r.status_code == 200)

        new_len_clients = len(json_data_get["clients"])

        # Comprobamos que el numero de clientes se mantiene igual despues de añadir y eliminar un cliente
        assert len_clients == new_len_clients

# Comprobacion del caso en el que el email pasado por parametros no exista
def test_client_delete_error1():

    with app.test_client() as c:
        # Intentamos borrar un cliente pasando un email erroneo
        r = c.delete('/client/me_lo_he_inventao@gmail.com', json={
            "password": "123456"
        })
        json_data = r.get_json()

        # Comprobamos si el estatus code es 404
        assert r.status_code == 404


# Comprobacion del caso en el que la contraseña pasada por el body no sea correcta
def test_client_delete_error2():

    with app.test_client() as c:

        # Creamos un cliente nuevo para que no haya conflictos con las reservas y starts
        r = c.post('/client', json={
            "nombre": "Test test test",
            "email": "test_delete_client3@gmail.com",
            "iban": "1234567890",
            "dni_nie": "12313312T",
            "password": "123456"
        })

        # Comprobamos si el estatus code es 201
        assert (r.status_code == 201)

        ################################################################################################################

        # Luego borramos el cliente creado anteriormente pero escribiendo mal la contraseña
        r = c.delete('/client/test_delete_client3@gmail.com', json={
            "password": "inventada"
        })
        json_data_delete = r.get_json()

        # Comprobamos si el estatus code es 500
        assert r.status_code == 500


# Comprobacion del caso en el que el cliente tenga un trayecto iniciado
def test_client_delete_error2():

    with app.test_client() as c:
        # Creamos un cliente nuevo para que no haya conflictos con las reservas y starts
        r = c.post('/client', json={
            "nombre": "Test test test",
            "email": "test_delete_client444@gmail.com",
            "iban": "12345647890",
            "dni_nie": "12314443312T",
            "password": "123456"
        })
        # Comprobamos si el estatus code es 201
        assert (r.status_code == 201)

        ################################################################################################################

        # Path POST moto reserve
        r = c.post('/reserve', json={
            "client_email": "test_delete_client444@gmail.com",
            "moto_id": 4
        })
        json_data_post = r.get_json()

        # Comprobamos si el estatus code es 201
        assert r.status_code == 201

        ################################################################################################################

        # Path POST moto start (client_email = juanita@gmail.com / moto_id = 1)
        r = c.post('/start', json={
            "client_email": "test_delete_client444@gmail.com",
            "moto_id": 4
        })
        json_data_post = r.get_json()

        # Comprobamos si el estatus code es 201
        assert r.status_code == 200

        ################################################################################################################

        # Luego borramos el cliente creado anteriormente pero escribiendo mal la contraseña
        r = c.delete('/client/test_delete_client444@gmail.com', json={
            "password": "inventada"
        })
        json_data_delete = r.get_json()

        # Comprobamos si el estatus code es 500
        assert r.status_code == 500

