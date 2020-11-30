from flask_restful import Resource, reqparse
from models.reserved_running_model import ReservedRunningModel
from models.client_model import ClientModel
from models.moto_model import MotoModel


class Reserved(Resource):
    def get(self, client_email):
        try:
            client = ClientModel.find_by_email(client_email)
            # Compruebo si ha encontrado el cliente con ese email
            if client is not None:
                rr = ReservedRunningModel.find_by_client(client.client_id)
                # Compruebo si ha encontrado la reserva del ciente
                if rr is not None:
                    # Compruebo el estado de la moto
                    if rr.isReserved():
                        # Compruebo que no se ha superado el tiempo limite para el start moto desde la reserva
                        if rr.check_remaining_time():
                            coord_client = (23.44333, 23.4433)
                            moto = rr.moto
                            moto_json = [moto.json_clientMoto()]
                            result = MotoModel.compute_distance(moto_json, coord_client, "distance")
                            # los cambios de keyname de jsons es para coordinar con frontend
                            return {'reserved_moto': result['motos'][0]}, 201
                        else:
                            ReservedRunningModel.update_state_available(rr)
                            ReservedRunningModel.delete_from_db(rr)
                            return {"message": "The time limit for the start has expired"}, 500
                    else:
                        return {"message": "ERROR RESERVED MOTO. Moto state isn't RESERVED, moto state = [{}]".format(rr.moto.state)}, 500
                else:
                    return {"message": "ERROR RESERVED MOTO. Error Client [{}] haven't reserved moto".format(client.client_id)}, 404
            else:
                return {"message": "ERROR RESERVED MOTO. Error Client Not Found"}, 404

        except:
            return {"message": "ERROR RESERVED MOTO. Error Get Reserved Moto"}, 500

    def post(self, client_email, moto_id):

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
                        remaining_time = rr.make_remaining_time()
                        return {"message": "You have until {}:{}h to start the motorbike".format(remaining_time.hour, remaining_time.minute),
                                "remaining_time": str(remaining_time.hour) + ":" + str(remaining_time.minute)}, 201
                    else:
                        return {"message": "ERROR RESERVED MOTO. Customer [{}] already has a reserved motorcycle".format(client.client_id)}, 500
                else:
                    return {"message": "ERROR RESERVED MOTO. Moto state isn't AVAILABLE, moto state = [{}]".format(moto.state)}, 500
            else:
                return {"message": "ERROR RESERVED MOTO. Motorcycle error or client not found for Reserved Moto post"}, 404


class Start(Resource):
    def get(self, client_email):
        try:
            client = ClientModel.find_by_email(client_email)
            if client is not None:
                rr = ReservedRunningModel.find_by_client(client.client_id)
                # Compruebo si ha encontrado la reserva del ciente
                if rr is not None:
                    # Compruebo si el estado de la moto es el correcto (ACTIVE)
                    if rr.isActive():
                        # Compruebo que no se ha superado el tiempo limite para el start moto desde la reserva
                        if rr.check_remaining_time():
                            coord_client = (23.44333, 23.4433)
                            moto = rr.moto
                            moto_json = [moto.json_clientMoto()]
                            result = MotoModel.compute_distance(moto_json, coord_client, "distance")
                            # los cambios de keyname de jsons es para coordinar con frontend
                            return {'start_moto': result['motos'][0]}, 201
                        else:
                            ReservedRunningModel.update_state_available(rr)
                            ReservedRunningModel.delete_from_db(rr)
                            return {"message": "The time limit for the start has expired"}, 500
                    else:
                        return {'message': "Error Moto state isn't active"}, 500
                else:
                    return {'message': "Error Client haven't start moto"}, 404
            else:
                return {'message': "Error Client Not Found"}, 404
        except:
            return {"message": "Error Get Start Moto"}, 500

    def post(self, client_email, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            client = ClientModel.find_by_email(client_email)
            rr = ReservedRunningModel.find_by_client_moto(client.client_id, moto_id)
            # Compruebo si existe el cliente segun el email recibido y si existe la moto segun el id recibido
            if moto is not None and client is not None:
                # Compruebo si el estado de la moto es el correcto (RESERVED)
                if moto.state == 'RESERVED':
                    # Compruebo si ha encontrado la reserva del ciente y la moto
                    if rr is not None:
                        # Compruebo que no se ha superado el tiempo limite para el start moto desde la reserva
                        if rr.check_remaining_time():
                            ReservedRunningModel.make_star_moto(rr)
                            ReservedRunningModel.update_state_start(rr)
                            return {"message": "Start successfully"}, 200
                        else:
                            ReservedRunningModel.update_state_available(rr)
                            ReservedRunningModel.delete_from_db(rr)
                            return {"message": "The time limit for the start has expired"}, 500
                    else:
                        return {"message": "Reservation error with that id_client and id_moto does not exist"}, 500
                else:
                    return {"message": "Error state moto isn't RESERVED"}, 500
            else:
                return {"message": "Motorcycle or client not found error for POST Start Moto"}, 404
        except:
            return {"message": "Error POST Start Moto"}, 500

