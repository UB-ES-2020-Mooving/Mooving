from flask_restful import Resource, reqparse
from models.mechanic_model import MechanicModel


class Mechanic(Resource):
    def get(self, id):
        try:
            mechanic = MechanicModel.find_by_id(id)
            return {'mechanic': mechanic.json()}, 200
        except:
            return {"message": "Error Get Mechanic"}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be left blank")
        parser.add_argument('subname', type=str, required=True, help="Subname cannot be left blank")
        parser.add_argument('dni', type=str, required=True, help="DNI cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be left blank")
        parser.add_argument('date_registration', type=str, required=True, help="Date Registration cannot be left blank")
        data = parser.parse_args()

        try:
            mechanic = MechanicModel(data['name'], data['subname'], data['dni'], data['password'], data['date_registration'])
            MechanicModel.save_to_db(mechanic)
            return {"message": "Mechanic added successfully"}, 200
        except:
            return {"message": "Error Post Mechanic"}, 500

    def delete(self, id):
        try:
            mechanic = MechanicModel.find_by_id(id)
            if mechanic:
                MechanicModel.delete_from_db(mechanic)
                return {"message": "Mechanic deleted"}, 200
            return {"message": "Mechanic not found "}, 404
        except:
            return {"message": "Error Delete Mechanic"}, 500

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('subname', type=str, required=False)
        parser.add_argument('password', type=str, required=False)
        data = parser.parse_args()

        try:
            mechanic = MechanicModel.find_by_id(id)
            if data['name']:
                mechanic.set_name(data['name'])
            if data['subname']:
                mechanic.set_subname(data['subname'])
            if data['password']:
                mechanic.set_password(data['password'])

            return {"message": "Mechanic modified successfully"}, 200
        except:
            return {"message": "Error Put Mechanic"}, 500


class MechanicList(Resource):
    def get(self):
        data = {'mechanics': []}
        mechanics = MechanicModel.get_all()
        for m in mechanics:
            data['mechanics'].append(m.json())
        return data
