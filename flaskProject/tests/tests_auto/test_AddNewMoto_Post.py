from tests.tests_auto.config_tests import *
from models.moto_model import MotoModel


def test_AddNewMoto_0_GoodRequest():
    with app.test_client() as c:
        path = '/moto'
        params = {
            "license_plate": "4321-PPP",
            "model_generic": "basic"
        }

        # No me preguntes porqué pero hace falta hacer una llamada (la primera vez) antes de acceder a MotoModel
        # Supongo que la App no se inicializa hasta que hago una llamada de algún tipo.
        c.get(path)

        # Nos aseguramos de que no esté en la DB
        db_moto = MotoModel.query.filter(MotoModel.matricula == params["license_plate"]).first()
        if db_moto is not None:
            db_moto.delete_from_db()
        # Request
        r = c.post(path, json=params)
        # Comprobaciones
        assert r.status_code == 200
        db_moto = MotoModel.query.filter(MotoModel.matricula == params["license_plate"]).first()
        assert db_moto is not None
        assert db_moto.model_generic == params["model_generic"]

        # Finalmente lo limpiamos para asegurarnos de que no queda nada.
        db_moto.delete_from_db()

def test_AddNewMoto_1_NoParams():
    with app.test_client() as c:
        path = '/moto'
        params = {
        }
        r = c.post(path, json=params)

        assert r.status_code == 400

def test_AddNewMoto_2_ExistingLicensePlate():
    with app.test_client() as c:
        path = '/moto'


        # No me preguntes porqué pero hace falta hacer una llamada (la primera vez) antes de acceder a MotoModel
        # Supongo que la App no se inicializa hasta que hago una llamada de algún tipo.
        c.get(path)

        # Cogemos una moto de la base de datos
        db_moto = MotoModel.query.first()

        if db_moto is None:
            # El test presupone una base de datos no vacía
            assert False

        # Cogemos una matrícula ya existente
        params = {
            "license_plate": db_moto.matricula,
            "model_generic": "basic"
        }
        r = c.post(path, json=params)

        # Comprobaciones
        # status code de que ya existe
        assert r.status_code == 409


def test_AddNewMoto_3_BadLicensePlateFormat():
    with app.test_client() as c:
        path = '/moto'
        params = {
            "license_plate": "4321-PP",
            "model_generic": "basic"
        }
        r = c.post(path, json=params)

        # Comprobaciones
        assert r.status_code == 400


def test_AddNewMoto_4_BadModelGenericFormat():
    with app.test_client() as c:
        path = '/moto'
        params = {
            "license_plate": "4321-PPP",
            "model_generic": "xxxxxx"
        }
        r = c.post(path, json=params)

        # Comprobaciones
        assert r.status_code == 400
