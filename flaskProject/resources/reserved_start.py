from flask_restful import Resource, reqparse
from models.reserved_running_model import ReservedRunningModel
from models.client_model import ClientModel
from models.moto_model import MotoModel
from sqlalchemy import and_, or_


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
                    # Compruebo si el cliente no tiene motos reservadas
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

    def delete(self, client_email, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            client = ClientModel.find_by_email(client_email)
            # En caso de que tanto la moto y el cliente existan en sus respectivas tablas
            if moto is not None and client is not None:
                moto = MotoModel.find_by_id(moto_id)
                client = ClientModel.find_by_email(client_email)
                # Compruebo si existe el cliente segun el email recibido y si existe la moto segun el id recibido
                if moto is not None and client is not None:
                    reserve = ReservedRunningModel.query.filter(and_(
                        ReservedRunningModel.clientId == client.client_id,
                        ReservedRunningModel.motoId == moto_id
                    )).first()
                    # Si no se encuentra la reserva con esas características...
                    if reserve is None:
                        return {"message": "DELETE ERROR. Moto reserved with id {} and client {} not found.".format(
                            moto_id, client_email)}, 404
                    # En caso de que si que exista una fila en la tabla RR...
                    else:
                        # Comprobamos cual es el auténtico estado de la moto.

                        # una reserva(state =="RESERVED"),
                        if moto.state == 'RESERVED':
                            # Borramos la fila de rr
                            reserve.delete_from_db()
                            # Actualizamos el estado de la moto
                            moto.state = "AVAILABLE"
                            moto.save_to_db()
                            return {"message": "Reserved Moto DELETED successfully"}, 200
                        # una running (state =="ACTIVE")
                        elif moto.state == 'ACTIVE':
                            # No se puede cancelar la reserva si no está reservada, sinó running(ACTIVE)
                            return {"message": "DELETE ERROR Moto Reserve: Moto is ACTIVE"}, 500
                        # un DESASTRE (state ==otra cosa, que no debería).
                        else:
                            # ¡¡¡¡ERROR FATAL!!!!
                            # Si entramos en este else es que la moto no debería estar en esta tabla.
                            # TODO Revisar si deberíamos borrarlo igualmente
                            return {"message": "FATAL Error. DELETE Moto Reserve: Moto is {}.".format(moto.state)}, 500
            # En caso de que o la moto o el cliente NO EXISTAN en sus respectivas tablas
            else:
                return {"message": "DELETE ERROR Moto Reserve. Moto with id [{}] or client with email [{}] not found."
                    .format(moto_id, client_email)}, 404
        except:
            return {"message": "DELETE ERROR Reserved Moto. Internal Failure."}, 500


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
