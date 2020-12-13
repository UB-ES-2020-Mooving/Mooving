from flask_restful import Resource, reqparse
from models.reserved_running_model import ReservedRunningModel
from models.client_model import ClientModel
from models.moto_model import MotoModel
from sqlalchemy import and_


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

                            remaining_time = rr.make_remaining_time()
                            if remaining_time.minute < 10:
                                time_min = "0" + str(remaining_time.minute)
                            else:
                                time_min = str(remaining_time.minute)
                            if remaining_time.hour < 10:
                                time_h = "0" + str(remaining_time.hour)
                            else:
                                time_h = str(remaining_time.hour)

                            return {'reserved_moto': result['motos'][0],
                                    "message": "You have until {}:{}h to start the motorbike".format(time_h, time_min),
                                    "remaining_time": time_h + ":" + time_min}, 201
                        else:
                            ReservedRunningModel.update_state_available(rr)
                            ReservedRunningModel.delete_from_db(rr)
                            return {"message": "The time limit for the start has expired"}, 500
                    else:
                        return {"message": "ERROR RESERVED MOTO. Moto state isn't RESERVED, moto state = [{}]".format(
                            rr.moto.state)}, 500
                else:
                    return {"message": "ERROR RESERVED MOTO. Error Client [{}] haven't reserved moto".format(
                        client.client_id)}, 404
            else:
                return {"message": "ERROR RESERVED MOTO. Error Client Not Found"}, 404

        except:
            return {"message": "ERROR RESERVED MOTO. Error Get Reserved Moto"}, 500

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('client_email', type=str, required=True, help="Client email cannot be left blank")
        parser.add_argument('moto_id', type=int, required=True, help="Moto id cannot be left blank")
        data = parser.parse_args()

        client_email = data['client_email']
        moto_id = data['moto_id']

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

                    remaining_time = rr.make_remaining_time()
                    if remaining_time.minute < 10:
                        time_min = "0" + str(remaining_time.minute)
                    else:
                        time_min = str(remaining_time.minute)
                    if remaining_time.hour < 10:
                        time_h = "0" + str(remaining_time.hour)
                    else:
                        time_h = str(remaining_time.hour)

                    return {"message": "You have until {}:{}h to start the motorbike".format(time_h, time_min),
                            "remaining_time": time_h + ":" + time_min}, 201
                else:
                    return {"message": "ERROR RESERVED MOTO. Customer [{}] already has a reserved motorcycle".format(
                        client.client_id)}, 500
            else:
                return {"message": "ERROR RESERVED MOTO. Moto state isn't AVAILABLE, moto state = [{}]".format(
                    moto.state)}, 500
        else:
            return {"message": "ERROR RESERVED MOTO. Motorcycle error or client not found for Reserved Moto post"}, 404

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

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('client_email', type=str, required=True, help="Client email cannot be left blank")
            parser.add_argument('moto_id', type=int, required=True, help="Moto id cannot be left blank")
            data = parser.parse_args()

            client_email = data['client_email']
            moto_id = data['moto_id']

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

    def put(self, client_email, moto_id):

        try:
            moto = MotoModel.query.filter(MotoModel.id == moto_id).first()
            client = ClientModel.query.filter(ClientModel.email == client_email).first()

            if moto is not None and client is not None:
                r = ReservedRunningModel.query.filter(and_(
                        ReservedRunningModel.motoId == moto_id,
                        ReservedRunningModel.clientId == client.client_id)).first()
                if r is not None and moto.state == "ACTIVE":
                    # En caso de que exista y de que este ACTIVE

                    # Aquí simulamos un par de cosas para aumentar el realismo de la versión de prueba

                    # Unas nuevas coordenadas (Aleatorias)
                    new_coord = MotoModel.get_random_coordinates()
                    # Calculamos los km_recorridos basándonos en las coordenadas
                    # (y poniendo un extra random, suponiendo trayectorias no rectas).
                    km_recorridos = moto.compute_km_recorridos(new_coord)

                    # Actualizamos todó lo necesario
                    moto.km_totales += km_recorridos
                    moto.km_restantes -= km_recorridos
                    if moto.hasLowBattery():
                        moto.state = 'LOW_BATTERY_FUEL'
                    else:
                        moto.state = "AVAILABLE"
                    moto.updateCoordAndAddress(new_coord)

                    r.delete_from_db()

                    return {'message_status': 'Ok',
                            'message': 'Motorbike stoped successfully'},200

            return {'message_status': "Not Found",
                    'message': "Client with email {} is not riding motorbike with id [{}]. "
                    .format(client_email, moto_id)}, 404

        except:
            return {'message_status': "Internal Error",
                    'message': "Internal Server Error. "}, 500
