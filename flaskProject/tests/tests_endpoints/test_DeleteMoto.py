from tests.tests_auto.config_tests import *
from models.moto_model import MotoModel

matricula = "3839-MMM"


def primera_llamada(c):
    # Esta funcion solo se usa porque ahora mismo no se puede llamar
    # a las tablas (ejemplo MotoModel.query....), si no se ha hecho una llamada
    # antes a algún resource.
    c.get("/motos")


def create_test_moto():
    new_moto = MotoModel.query.filter(MotoModel.matricula == matricula).first()
    # Si ya existe retornamos directamente
    if new_moto is not None:
        return new_moto
    # Si no existe la creamos
    new_moto = MotoModel(
        state="AVAILABLE",
        matricula=matricula,
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4434,
        last_coordinate_longitude=23.4433,
        km_restantes=120.0,
        km_totales=500.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    new_moto.save_to_db()

    new_moto = MotoModel.query.filter(MotoModel.matricula == matricula).first()

    if new_moto is None:
        # No se ha añadido a la base de datos!!!!
        # Si esto no funciona los tests no tienen sentido.
        assert False
    return new_moto


def delete_test_moto():
    new_moto = MotoModel.query.filter(MotoModel.matricula == matricula).first()
    # Si aún existe la borramos.
    if new_moto is not None:
        new_moto.delete_from_db()


def test_DeleteMoto_0_GoodRequest():
    with app.test_client() as c:
        # Hay que hacer esto por ahora, dado que sino falla
        primera_llamada(c)

        # Creo una moto
        new_moto = create_test_moto()

        id_moto = new_moto.id
        path = "/moto/" + str(id_moto)
        r = c.delete(path)
        json_data = r.get_json()

        expected_keys = {"message", "message_status"}
        # Lo pongo con un set pq no nos importa el orden.
        assert set(json_data.keys()) == expected_keys
        assert r.status_code == 200
        # Nos aseguramos de que se borre
        delete_test_moto()


def test_DeleteMoto_1_NotFound():
    with app.test_client() as c:
        # Hay que hacer esto por ahora, dado que sino falla
        primera_llamada(c)

        # Suponiendo que no hay ninguna moto con id = 1 billón
        id_moto = 1000000000
        moto = MotoModel.query.filter(MotoModel.id == id_moto).first()
        # Mientras la moto NO sea None, buscamos otro id
        while moto is not None:
            id_moto += 50
            moto = MotoModel.query.filter(MotoModel.id == id_moto).first()

        path = "/moto/" + str(id_moto)
        r = c.delete(path)
        json_data = r.get_json()

        expected_keys = {"message", "message_status"}
        # Lo pongo con un set pq no nos importa el orden.
        assert set(json_data.keys()) == expected_keys
        assert r.status_code == 404


def test_DeleteMoto_2_BadPath():
    with app.test_client() as c:
        # Path incorrecto.
        path = "/moto"
        r = c.delete(path)
        assert r.status_code == 500


def test_DeleteMoto_3_ReservedMoto():
    with app.test_client() as c:
        # Hay que hacer esto por ahora, dado que sino falla
        primera_llamada(c)

        # Creo una moto
        new_moto = create_test_moto()

        new_moto.state = "RESERVED"
        new_moto.save_to_db()

        id_moto = new_moto.id
        path = "/moto/" + str(id_moto)
        r = c.delete(path)
        json_data = r.get_json()

        expected_keys = {"message", "message_status"}
        # Lo pongo con un set pq no nos importa el orden.
        assert set(json_data.keys()) == expected_keys
        assert r.status_code == 409
        # Nos aseguramos de que se borre
        delete_test_moto()


def test_DeleteMoto_4_ActiveMoto():
    with app.test_client() as c:
        # Hay que hacer esto por ahora, dado que sino falla
        primera_llamada(c)

        # Creo una moto
        new_moto = create_test_moto()

        new_moto.state = "ACTIVE"
        new_moto.save_to_db()

        id_moto = new_moto.id
        path = "/moto/" + str(id_moto)
        r = c.delete(path)
        json_data = r.get_json()

        expected_keys = {"message", "message_status"}
        # Lo pongo con un set pq no nos importa el orden.
        assert set(json_data.keys()) == expected_keys
        assert r.status_code == 409
        # Nos aseguramos de que se borre
        delete_test_moto()
