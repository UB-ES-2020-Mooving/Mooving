import math

import app
from models.moto_model import MotoModel

# Test

m1 = MotoModel(
    state="ACTIVE",
    matricula="3333-MMM",
    date_estreno="28/10/2020",
    model_generic="premium",
    last_coordinate_latitude=23.,
    last_coordinate_longitude=23.,
    km_restantes=120.0,
    km_totales=0.0,
    date_last_check="18/10/2020",
    km_last_check=0.0)

m2 = MotoModel(
    state="ACTIVE",
    matricula="4444-MMM",
    date_estreno="28/10/2020",
    model_generic="premium",
    last_coordinate_latitude=23.1,
    last_coordinate_longitude=23.1,
    km_restantes=120.0,
    km_totales=0.0,
    date_last_check="18/10/2020",
    km_last_check=0.0)

m3 = MotoModel(
    state="LOW_BATTERY_FUEL",
    matricula="5555-MMM",
    date_estreno="08/10/2020",
    model_generic="premium",
    last_coordinate_latitude=23.2,
    last_coordinate_longitude=23.2,
    km_restantes=30.0,
    km_totales=100.0,
    date_last_check="18/10/2020",
    km_last_check=100.0)

m4 = MotoModel(
    state="LOW_BATTERY_FUEL",
    matricula="6666-MMM",
    date_estreno="08/10/2020",
    model_generic="premium",
    last_coordinate_latitude=23.3,
    last_coordinate_longitude=23.3,
    km_restantes=30.0,
    km_totales=100.0,
    date_last_check="18/10/2020",
    km_last_check=100.0)




def test_ClientMotoList1_Basico():
    lista_motos = [m1, m2, m3, m4]
    json_motos = [m.json_listmotos() for m in lista_motos]

    keyword = "distance"
    coord = (22.9, 22.9)
    respuesta = MotoModel.compute_distance(json_motos, coord, keyword)
    assert "motos" in respuesta.keys()
    dist_anterior = 0
    for r in respuesta["motos"]:
        distancia = r[keyword]
        # Esto es que está ordenada la lista
        assert dist_anterior <= distancia
        # Esto es que esté redondeado sin decimales
        assert distancia % 1 == 0
        dist_anterior = distancia


def test_ClientMotoList2_Distancia():
    lista_motos = [m1, m2, m3, m4]
    json_motos = [m.json_listmotos() for m in lista_motos]

    keyword = "distance"
    distancia_maxima = 35000
    coord = (22.9, 22.9)
    respuesta = MotoModel.compute_distance(json_motos, coord, keyword, distancia_maxima)
    assert "motos" in respuesta.keys()
    dist_anterior = 0
    for r in respuesta["motos"]:
        distancia = r[keyword]
        # Esto es que está ordenada la lista
        assert dist_anterior <= distancia
        assert distancia <= distancia_maxima
        # Esto es que esté redondeado sin decimales
        assert distancia % 1 == 0
        dist_anterior = distancia


def test_ClientMotoList3_DistanciaMaximaPequeña():
    lista_motos = [m1, m2, m3, m4]
    json_motos = [m.json_listmotos() for m in lista_motos]

    keyword = "distance"
    distancia_maxima = 100
    coord = (22.9, 22.9)
    respuesta = MotoModel.compute_distance(json_motos, coord, keyword, distancia_maxima)
    assert "motos" in respuesta.keys()
    #esperamos una lista vacía, dado que la distancia es menor que la mínima
    assert len(respuesta["motos"]) == 0
def test_ClientMotoList4_EntradaVacia():
    lista_motos = []
    json_motos = [m.json_listmotos() for m in lista_motos]

    keyword = "distance"
    distancia_maxima = 100000000
    coord = (22.9, 22.9)
    respuesta = MotoModel.compute_distance(json_motos, coord, keyword, distancia_maxima)
    assert "motos" in respuesta.keys()
    #esperamos una lista vacía, dado que la distancia es menor que la mínima
    assert len(respuesta["motos"]) == 0

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