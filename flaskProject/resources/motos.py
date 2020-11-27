from flask_restful import Resource, reqparse
from models.moto_model import MotoModel

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
        parser.add_argument('state', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('matricula', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('date_estreno', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('model_generic', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('last_coordinate_latitude', type=float, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('last_coordinate_longitude', type=float, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('km_restantes', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('km_totales', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('date_last_check', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            moto = MotoModel(data['state'], data['matricula'], data['date_estreno'], data['model_generic'],
                             data['last_coordinate_latitude'],
                             data['last_coordinate_longitude'], data['km_restantes'], data['km_totales'],
                             data['date_last_check'])
            MotoModel.save_to_db(moto)
            return {"message": "Moto added successfully"}, 200
        except:
            return {"message": "Error Post Moto"}, 500

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
        parser.add_argument('state', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('matricula', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('date_estreno', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('model_generic', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('last_coordinate_latitude', type=float, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('last_coordinate_longitude', type=float, required=True,
                            help="This field cannot be left blank")
        parser.add_argument('km_restantes', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('km_totales', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('date_last_check', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            moto = MotoModel.find_by_id(id)
            moto.set_moto(data['state'], data['matricula'], data['date_estreno'], data['model_generic'],
                          data['last_coordinate_latitude'],
                          data['last_coordinate_longitude'], data['km_restantes'], data['km_totales'],
                          data['date_last_check'])
            MotoModel.save_to_db(moto)
            return {"message": "Moto modified successfully"}, 200
        except:
            return {"message": "Error Put Moto"}, 500


class ClientMotosList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('model_generic', type=str)
        parser.add_argument('more_km_restantes', type=int)

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
        coord_client = (23.44333, 23.4433)
        data = {'motos': []}
        motos = MotoModel.get_all()
        motos_json = [m.json_mechaniclistmotos() for m in motos]
        result = MotoModel.compute_distance(motos_json, coord_client, "distance")
        return result
