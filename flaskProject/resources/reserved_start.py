from flask_restful import Resource, reqparse
from models.reserved_running_model import ReservedRunningModel
from models.client_model import ClientModel
from models.moto_model import MotoModel


class Reserved(Resource):
    def get(self, id):
        try:
            rr = ReservedRunningModel.find_by_id(id)
            return {'reserved_moto': rr.json_reserved()}, 200
        except:
            return {"message": "Error Get Reserved Moto"}, 500


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
                        return {"message": "reserved added successfully"}, 200
                    else:
                        return {"message": "Customer error already has a reserved motorcycle"}, 500
                else:
                    return {"message": "Error state moto isn't AVAILABLE"}, 500
            else:
                return {"message": "Motorcycle error or client not found for Reserved Moto post"}, 404
        except:
            return {"message": "Error Post Reserved Moto"}, 500


class Start(Resource):
    def get(self, id):
        try:
            rr = ReservedRunningModel.find_by_id(id)
            return {'start_moto': rr.json_start()}, 200
        except:
            return {"message": "Error Get Start Moto"}, 500

    def post(self, client_email, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            client = ClientModel.find_by_email(client_email)
            rr = ReservedRunningModel.find_by_client_moto(client.client_id, moto_id)
            # Compruebo si existe el cliente segun el email recibido y si existe la moto segun el id recibido
            if moto is not None and client is not None:
                if moto.state == 'RESERVED':
                    if rr is not None:
                        ReservedRunningModel.make_star_moto(rr)
                        ReservedRunningModel.update_state_start(rr)
                        return {"message": "Start successfully"}, 200
                    else:
                        return {"message": "Reservation error with that id_client and id_moto does not exist"}, 500
                else:
                    return {"message": "Error state moto isn't RESERVED"}, 500
            else:
                return {"message": "Motorcycle or client not found error for POST Start Moto"}, 404
        except:
            return {"message": "Error POST Start Moto"}, 500

