from db import db
from flask_restful import Resource, reqparse
from models.client_model import ClientModel

class Clients(Resource):
    def get(self, client_id):
        c = ClientModel.query.filter_by(client_id=client_id).first()
        if c:
            return {'client':c.json()}, 200
        else:
            return {'message': 'There is no client with ID [{}] .'.format(client_id)}, 404

    def post(self, client_id = None):

        #Creamos el request parser, que nos ayudará a manejar la informacion de entrada
        parser = reqparse.RequestParser()
        #Definimos que esperamos como entrada
        parser.add_argument('nombre', type=str,required=True, help="Name field cannot be left blanck")
        parser.add_argument('email', type=str,required=True, help="Email field cannot be left blanck")
        parser.add_argument('iban', type=str,required=True, help="IBAN field cannot be left blanck")
        parser.add_argument('genero', type=str,required=True, help="Genre field cannot be left blanck")
        parser.add_argument('dni_nie', type=str,required=True, help="DNI/NIE field cannot be left blanck")
        parser.add_argument('password', type=str, required=True, help="Password field cannot be left blanck")
        #Tomamos la información del parser en un diccionario (data)
        data = parser.parse_args()

        c = ClientModel.query.filter_by(email=data['email']).first()
        if c:
            return {'message': 'A client with same email [{}] already exists'.format(data['email'])}, 400

        c = ClientModel.query.filter_by(dni_nie=data['dni_nie']).first()
        if c:
            return {'message': 'A client with same DNI/NIE [{}] already exists'.format(data['dni_nie'])}, 400

        entry = ClientModel(data['nombre'],data['genero'],data['iban'],data['dni_nie'],data['email'],data['password'])
        entry.save_to_db()

        return entry.json(), 201

    def delete(self, client_id):
        c = ClientModel.query.filter_by(client_id=client_id).first()
        if c:
            c.delete_from_db()
            return {'message': 'Client with ID [{}] correctly deleted.'.format(client_id)}, 200
        else:
            return {'message': 'There is no client with ID [{}] .'.format(client_id)}, 404

    def put(self, client_id):
        # Creamos el request parser, que nos ayudará a manejar la informacion de entrada
        parser = reqparse.RequestParser()
        # Definimos que esperamos como entrada
        parser.add_argument('nombre', type=str, required=True, help="Name field cannot be left blanck")
        parser.add_argument('email', type=str, required=True, help="Email field cannot be left blanck")
        parser.add_argument('iban', type=str, required=True, help="IBAN field cannot be left blanck")
        parser.add_argument('genero', type=str, required=True, help="Genre field cannot be left blanck")
        # Tomamos la información del parser en un diccionario (data)
        data = parser.parse_args()

        c = ClientModel.query.filter_by(client_id=client_id).first()
        if c:
            c.nombre = data['nombre']
            c.email = data['email']
            c.iban = data['iban']
            c.genero = data['genero']
            c.save_to_db()

            return c.json(), 200
        else:
            return {'message': 'There is no client with ID [{}] .'.format(client_id)}, 404

class ClientsList(Resource):
    def get(self):
        clients=ClientModel.query.filter_by().all()
        data ={'clients':[]}
        for c in clients:
            data['clients'].append(c.json())

        return data


