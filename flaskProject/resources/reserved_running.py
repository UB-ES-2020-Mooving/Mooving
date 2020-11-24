from flask_restful import Resource, reqparse
from models.reserved_running_model import ReservedRunningModel
from models.client_model import ClientModel
from models.moto_model import MotoModel


class ReservedRunning(Resource):
    def get(self, id):
        try:
            rr = ReservedRunningModel.find_by_id(id)
            return {'reserved_running': rr.json()}, 200
        except:
            return {"message": "Error Get RR"}, 500

    def post(self, client_email, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            client = ClientModel.find_by_email(client_email)
            # Compruebo si existe el cliente segun el email recibido y si existe la moto segun el id recibido
            if moto is not None and client is not None:
                # Compruebo si el estado de la moto es el correcto (AVAILABLE)
                if moto.state == 'AVAILABLE':
                    #Compruebo si el cliente no tiene motos reservadas
                    if ReservedRunningModel.find_by_client(client.client_id) is None:
                        rr = ReservedRunningModel(client, moto)
                        ReservedRunningModel.save_to_db(rr)
                        ReservedRunningModel.update_state_reserved(rr)
                        return {"message": "RR added successfully"}, 200
                    else:
                        return {"message": "Error cliente ya tiene moto reservada"}, 500
                else:
                    return {"message": "Error estado moto"}, 500
            else:
                return {"message": "Error moto o cliente no encontrados para post RR"}, 500
        except:
            return {"message": "Error Post RR"}, 500

    def put(self, client_email, moto_id):

        moto = MotoModel.find_by_id(moto_id)
        client = ClientModel.find_by_email(client_email)
        rr = ReservedRunningModel.find_by_client_moto(client.client_id, moto_id)
        # Compruebo si existe el cliente segun el email recibido y si existe la moto segun el id recibido
        if moto is not None and client is not None:
            if rr is not None:
                ReservedRunningModel.make_star_moto(rr)
                ReservedRunningModel.update_state_active(rr)
                return {"message": "RR modified successfully"}, 200
            else:
                return {"message": "Error reserva con ese id_client e id_moto no existe"}, 500
        else:
            return {"message": "Error moto o cliente no encontrados para put RR"}, 500


