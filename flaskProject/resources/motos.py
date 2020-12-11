from flask_restful import Resource, reqparse
from models.moto_model import MotoModel
from datetime import datetime
import random
from sqlalchemy import and_, or_


class Moto(Resource):
    def get(self, id):
        try:
            moto = MotoModel.find_by_id(id)
            return {'moto': moto.json()}, 200
        except:
            return {"message": "Error Get Moto"}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('license_plate', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('model_generic', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        matricula = data["license_plate"].upper()
        model_generic = data["model_generic"]

        if not MotoModel.is_license_plate(matricula):
            return {"message": "ERROR: The format of the license plate is not valid."}, 400
        if model_generic not in ("basic", "premium"):
            return {"message": "ERROR: model_generic should be either [basic] or [premium]."}, 400

        m = MotoModel.query.filter(MotoModel.matricula == data["license_plate"]).first()
        if m is not None:
            return {"message": "There is already a motorbike with license plate [{}].".format(matricula)}, 409
        else:
            try:
                date_format = "%d/%m/%Y"
                today = datetime.now().strftime(date_format)
                str_today = today#str(today.day) + str(today.month) + str(today.year)

                # Esto de aquí genera unas coordenadas en BCN con ruido gausiano.
                latt, long = MotoModel.get_random_coordinates()

                moto = MotoModel('AVAILABLE', matricula, str_today, data['model_generic'],
                                 latt, long, 50, 0, str_today, 0)
                moto.save_to_db()
                return {"message": "Moto added successfully"}, 200
            except:
                return {"message": "Internal Error Post Moto"}, 500

    def delete(self, id):
        try:
            moto = MotoModel.find_by_id(id)
            if moto:
                MotoModel.delete_from_db(moto)
                return {"message": "Moto deleted"}, 200
            return {"message": "Moto not found "}, 404
        except:
            return {"message": "Error Delete Moto"}, 500

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('matricula', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('km_restantes', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('state', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        moto = MotoModel.find_by_id(id)
        if (moto):
            moto_aux = MotoModel.find_by_matricula(data['matricula'])
            if(moto.id != moto_aux.id):
                return {'message': "Motorbike with license plate [{}] already exists".format(data['matricula'])}, 409
            else:
                if((data['km_restantes'] <= 5.0 and data['state'] == "AVAILABLE") or (data['km_restantes'] > 5.0 and data['state'] == "LOW_BATTERY_FUEL")):
                    return {'message': "State and the battery fields are not consistent"}, 400
                try:
                    moto.set_moto(data['matricula'],data['km_restantes'],data['state'])
                    MotoModel.save_to_db(moto)
                    return {"message": "Motorbike modified successfully"}, 200
                except:
                    return {"message": "Error while trying to modify motorbike with id [{}]".format(id)}, 500

        else:
            return {'message': "Motorbike with id [{}] Not Found".format(id)}, 404


class ClientMotosList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('model_generic', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('more_km_restantes', type=int, required=True, help="This field cannot be left blank")

        # Parámetros que pueden ser útiles en el futuro:
        # parser.add_argument('client_coordinate_latitude', type=float, required=True,help="This field cannot be left blank")
        # parser.add_argument('client_coordinate_longitude', type=float, required=True,help="This field cannot be left blank")
        # parser.add_argument('max_distance_m', type=float)

        data = parser.parse_args()

        # coord_client = (data["client_coordinate_latitude"], data["client_coordinate_longitude"])
        coord_client = (23.44333, 23.4433)

        # Aquí se empieza con las condiciones resultantes de los filtros.
        list_and = []

        # Para el cliente siempre queremos las ACTIVE
        # (creo que se tiene que cambiar por AVAILABLE en algun momento)
        list_and.append(MotoModel.state == "AVAILABLE")

        # El caso sin filtro es data["more_km_restantes"]==0
        if data["more_km_restantes"] > 0:
            list_and.append(MotoModel.km_restantes > data["more_km_restantes"])

        # El caso sin filtro es data["model_generic"]=="all"
        if data["model_generic"] in ("premium", "basic"):
            list_and.append(MotoModel.model_generic == data['model_generic'])

        # En esta función juntamos todas las condiciones en una sucesión de AND's
        cond_final = MotoModel.condiciones_AND(list_and)

        # Hacemos la query en base a los filtros (condiciones previas)
        motos = MotoModel.query.filter(cond_final).all()

        # Hacemos una lista de jsons para enviarselo a la funcion compute_distance
        motos_json = [m.json_listmotos() for m in motos]

        # Calculamos las distancias y las añadimos a cada moto
        result = MotoModel.compute_distance(motos_json, coord_client, "distance")

        return result


class MechanicMotosList(Resource):
    def get(self):
        coord_mechanic = (23.44333, 23.4433)
        motos = MotoModel.get_all()
        motos_json = [m.json_mechaniclistmotos() for m in motos]
        result = MotoModel.compute_distance(motos_json, coord_mechanic, "distance")
        return result


# informacion de un moto en concreto para cliente
class ClientMoto(Resource):
    def get(self, id):
        coord_client = (23.44333, 23.4433)
        try:
            moto = MotoModel.find_by_id(id)
            moto_json = [moto.json_clientMoto()]
            result = MotoModel.compute_distance(moto_json, coord_client, "distance")
            # los cambios de keyname de jsons es para coordinar con frontend
            return {'client_moto': result['motos'][0]}, 200
        except:
            return {"message": "Error Get Moto"}, 500


# informacion de un moto en concreto para mechanic
class MechanicMoto(Resource):
    def get(self, id):
        coord_mechanic = (23.44333, 23.4433)
        try:
            moto = MotoModel.find_by_id(id)
            moto_json = [moto.json_mechanicMoto()]
            result = MotoModel.compute_distance(moto_json, coord_mechanic, "distance")
            # los cambios de keyname de jsons es para coordinar con frontend
            return {'mechanic_moto': result['motos'][0]}, 200
        except:
            return {"message": "Error Get Moto"}, 500
