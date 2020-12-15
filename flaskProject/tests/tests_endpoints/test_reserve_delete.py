from tests.tests_endpoints.config_tests import *
from models.reserved_running_model import ReservedRunningModel


# Este test presupone que el post funciona correctamente.
# En caso de que el post falle, este test también fallará.
def test_cancel_moto_reservation_0():
    with app.test_client() as c:
        # Me aseguro de que haya una reserva
        path = '/reserve'
        params = {
            'client_email': 'camila@gmail.com',
            'moto_id': 2
        }
        r = c.post(path, json=params)
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()
        # Si falla aquí, el post no funciona
        assert reserva is not None


        path = '/reserve/camila@gmail.com/2'
        r = c.delete(path)
        json_data = r.get_json()
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()

        assert reserva is None
        assert r.status_code == 200

def test_cancel_moto_reservation_2():
    with app.test_client() as c:
        # Me aseguro de que haya una reserva
        path = '/reserve'
        params = {
            'client_email': 'camila@gmail.com',
            'moto_id': 2
        }
        r = c.post(path, json=params)
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()
        # Si falla aquí, el post no funciona
        assert reserva is not None

        # El correo está equivocado
        path = '/reserve/c@gmail.com/2'
        r = c.delete(path)
        json_data = r.get_json()
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()

        assert reserva is not None
        assert r.status_code == 404

def test_cancel_moto_reservation_3():
    with app.test_client() as c:
        # Me aseguro de que haya una reserva
        path = '/reserve'
        params = {
            'client_email': 'camila@gmail.com',
            'moto_id': 2
        }
        r = c.post(path, json=params)
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()
        # Si falla aquí, el post no funciona
        assert reserva is not None

        # El moto_id está mal
        path = '/reserve/camila@gmail.com/1'
        r = c.delete(path)
        json_data = r.get_json()
        reserva = ReservedRunningModel.query.filter(ReservedRunningModel.motoId == 2).first()

        assert reserva is not None
        assert r.status_code == 404