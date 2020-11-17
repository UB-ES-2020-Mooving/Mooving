from flask_restful import Resource, reqparse
from models.moto_model import MotoModel
from geopy.distance import distance
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
        # parser.add_argument('client_coordinate_latitude', type=float, required=True,help="This field cannot be left blank")
        # parser.add_argument('client_coordinate_longitude', type=float, required=True,help="This field cannot be left blank")
        parser.add_argument('max_distance_m', type=float)
        data = parser.parse_args()

        # coord_client = (data["client_coordinate_latitude"], data["client_coordinate_longitude"])
        coord_client = (23.44333, 23.4433)

        # Si model generic no es None
        if data['model_generic']:
            # todo, comprobar que modelgeneric sea uno de los posibles y no cualquier cosa
            motos = MotoModel.query.filter(
                and_(MotoModel.model_generic == data['model_generic'], MotoModel.state == "ACTIVE")).all()
        else:
            motos = MotoModel.query.filter(MotoModel.state == "ACTIVE").all()

        motos_json = [m.json_listmotos() for m in motos]
        if data["max_distance_m"]:
            result = compute_distance(motos_json, coord_client, "distance", data["max_distance_m"])
        else:
            result = compute_distance(motos_json, coord_client, "distance")

        return result


class MechanicMotosList(Resource):
    def get(self):
        coord_client = (23.44333, 23.4433)
        data = {'motos': []}
        motos = MotoModel.get_all()
        motos_json = [m.json_mechaniclistmotos() for m in motos]
        result = compute_distance(motos_json, coord_client, "distance")
        return result


def compute_distance(motos, coord, key_name, max_dist=float("inf")):
    # Este bloque es para comprobar que la key_name no coincida con otra key del diccionario y falle.
    if len(motos) > 0:
        json = motos[0]
        if key_name in json.keys():
            raise NameError('key_name ERROR. key_name cannot be the same as other keys'
                            'in the JSON.')
    # Valor al que se redondea la distancia
    round_value = 1
    data = {'motos': []}
    for m in motos:
        distancia_metros = distance((m['last_coordinate_latitude'], m['last_coordinate_latitude']), coord).m
        m[key_name] = round(distancia_metros / round_value) * round_value
        # Si es menor que la máxima distancia lo metemos
        if m[key_name] < max_dist:
            data['motos'].append(m)

    data['motos'].sort(key=lambda x: x[key_name])

    return data
