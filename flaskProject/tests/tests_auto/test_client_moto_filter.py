from tests.tests_auto.config_tests import *
from models.moto_model import MotoModel

def test_client_moto_filter_0_BASE():
    with app.test_client() as c:
        model_generic = "all"
        more_km_restantes = 0
        path = '/motos'
        params = {
            "client_coordinate_latitude":41.387677,
            "client_coordinate_longitude":2.169320,
            "model_generic": model_generic,
            "more_km_restantes": more_km_restantes
        }
        r = c.get(path, json=params)
        json_data = r.get_json()
        assert r.status_code == 200


def test_client_moto_filter_1_GRID():
    with app.test_client() as c:
        model_generic_values = ["all", "basic", "premium"]
        more_km_restantes_values = [0, 50, 100, 200]
        for model_generic in model_generic_values:
            for more_km_restantes in more_km_restantes_values:

                path = '/motos'
                params = {
                    "client_coordinate_latitude": 41.387677,
                    "client_coordinate_longitude": 2.169320,
                    "model_generic": model_generic,
                    "more_km_restantes": more_km_restantes
                }
                r = c.get(path, json=params)
                json_data = r.get_json()
                assert r.status_code == 200
                assert 'motos' in json_data
                motos = json_data['motos']
                model = params["model_generic"]
                km = params["more_km_restantes"]
                expected_keys = ["id",
                                 "matricula",
                                 "model_generic",
                                 "km_restantes",
                                 "last_coordinate_latitude",
                                 "last_coordinate_longitude",
                                 "distance"]
                for m in motos:

                    # Ejemplo de una respuesta esperada
                    """
                    "id": 3,
                    "matricula": "3333-MMM",
                    "model_generic": "premium",
                    "km_restantes": 120.0,
                    "last_coordinate_latitude": 23.4434,
                    "last_coordinate_longitude": 23.4433,
                    "distance": 13
                    """

                    assert list(m.keys()) == expected_keys
                    moto_db = MotoModel.query.filter(MotoModel.id == m['id']).first()
                    assert moto_db is not None
                    assert moto_db.state == 'AVAILABLE'
                    if model in ["basic", "premium"]:
                        assert m["model_generic"] == model
                    if km != 0:
                        assert m["km_restantes"] > km
                    assert m["km_restantes"] > 0
def test_client_moto_filter_2_BAD_REQUEST():
    with app.test_client() as c:
        path = '/motos'
        params = {}
        r = c.get(path, json=params)
        assert r.status_code == 400

def test_client_moto_filter_3_BAD_REQUEST():
    with app.test_client() as c:
        model_generic = "all"
        path = '/motos'
        params = {
            "model_generic": model_generic
        }
        r = c.get(path, json=params)
        assert r.status_code == 400

def test_client_moto_filter_4_BAD_REQUEST():
    with app.test_client() as c:
        more_km_restantes = 0
        path = '/motos'
        params = {
            "more_km_restantes": more_km_restantes
        }
        r = c.get(path, json=params)
        assert r.status_code == 400

