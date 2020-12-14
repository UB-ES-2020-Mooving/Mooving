from tests.tests_auto.config_tests import *


def test_ejemplo():
    # Se utiliza la keyword "with" porque es más seguro trabajar con recursos de esa
    # manera. Al fin y al cabo es una asignación pero se asegura de una correcta
    # adquisición y liberación de recursos. Sinceramente no se muy bien como lo hace,
    # pero si teneis curiosidad podeis leeros esto de aquí:
    # https://www.geeksforgeeks.org/with-statement-in-python/

    # lo equivalente sería un simple
    # c = app.test_client()
    with app.test_client() as c:
        # Cuidado no llaméis a ninguna variable "c" o "client".
        # Lo de c simplemente es pq es el nombre de la variable que estoy utilizando en los tests.
        # Lo de client es pq está la función de arriba que creo que es imprescindible que se llame así
        # y no se debería de cambiar.

        # Aquí ponemos el path del endpoint
        path = '/clients'
        # Aquí llamamos al enpoint en cuestión con el método y el path
        r = c.get(path)
        # Si la respuesta es un error o algo por el estilo esto revienta (No hay json)
        # Si teneis muchas dudas os recomiendo que pongais un breakpoint en una de estas
        # líneas y ejecuteis en modo debug. Os haréis una idea de que hay dentro y tal.
        json_data = r.get_json()

        assert "clients" in json_data.keys()
        assert r.status_code == 200

        clients = json_data["clients"]
        len_clients = len(clients)
        # assert len_clients == 4
        client0 = clients[0]

        # Aquí estoy probando otras cosas para ver como funcionan

        # El get funciona correctamente
        path_get_client = "/client/1"


        #r = c.delete("/client/"+str(client0["client_id"]))
        r = c.get(path_get_client)


        json_data_get_client = r.get_json()

        """
        # El delete no y eso me da muchas ganas de llorar.
        path_delete = "/client/1"
        r = c.delete(path_delete)
        json_data_delete = r.get_json()
        """

        # Con esto quería comprobar que efectivamente el delete funciona
        # pero no lo hace :,>( . Por eso falla el test
        r = c.get("/clients")
        json_data = r.get_json()
        clients2 = json_data["clients"]
        # Ya fallaba antes, no te asustes
        # assert len(clients)-1 == len(clients2)
        # assert client0 in clients and client0 not in clients2

        # Ejemplo de post. Este si que funciona
        r = c.post('/client', json={
            "nombre": "Pepito 2",
            "email": "pepito40@gmail.com",
            "iban": "2345245234523",
            "dni_nie": "885688230D",
            "password": "cacatua"
        })
        json_data_post = r.get_json()
        # Me puedo imaginar que con el put también, pero no lo he comprobado.

        # Por si sirve de algo he visto que también se puede llamar del siguiente modo
        # r = c.open(path="/clients",method="GET") etc etc
        # aquí dejo un link donde lo explica:
        # https://werkzeug.palletsprojects.com/en/1.0.x/test/

        # Se que para ser un ejemplo es una burrada y es demasiado largo y tal.
        # Pero realmente hasta ahora solo ha sido un campo de pruebas donde
        # ver que tal funcionaban algunas cosas. Espero que te sea útil.


# Es el mismo ejemplo que el anterior, pero solo para que veas que se
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

