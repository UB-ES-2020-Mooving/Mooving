from flask_restful import Resource, reqparse
from models.moto_model import MotoModel
from geopy.distance import distance


class Moto(Resource):
    def get(self, id):
        try:
            moto = MotoModel.find_by_id(id)
            return {'moto':moto.json()}, 200
        except:
            return {"message": "Error Get Moto"}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('state', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('matricula', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('date_estreno', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('model_generic', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('last_coordinate_latitude', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('last_coordinate_longitude', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('km_restantes', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('km_totales', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('date_last_check', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            moto = MotoModel(data['state'], data['matricula'], data['date_estreno'], data['model_generic'], data['last_coordinate_latitude'],
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
            moto.set_moto(data['state'], data['matricula'], data['date_estreno'], data['model_generic'], data['last_coordinate_latitude'],
                               data['last_coordinate_longitude'], data['km_restantes'], data['km_totales'],
                              data['date_last_check'])
            MotoModel.save_to_db(moto)
            return {"message": "Moto modified successfully"}, 200
        except:
            return {"message": "Error Put Moto"}, 500

class MotosList(Resource):
    def get(self):
        coord_client = (23.4433, 23.4433)
        data = {'motos': []}
        motos = MotoModel.get_all()
        for m in motos:
            lista_motos = m.json_listmotos()
            lista_motos['distance_client'] = distance((m.get_last_coordinate_latitude(), m.get_last_coordinate_longitude()), coord_client).m
            data['motos'].append(lista_motos)

        data['motos'].sort(key=lambda x: x["distance_client"])
        return data
