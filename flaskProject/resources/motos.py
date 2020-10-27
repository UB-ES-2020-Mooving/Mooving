from flask_restful import Resource, reqparse


class Motos(Resource):
    def get(self, id):
        return {'message': "Get Not developed yet"}, 404

    def post(self):

        #Creamos el request parser, que nos ayudará a manejar la informacion de entrada
        parser = reqparse.RequestParser()
        #Definimos que esperamos como entrada
        parser.add_argument('state', type=str)

        #Tomamos la información del parser en un diccionario (data)
        data = parser.parse_args()

        return {'message':"No me gusta "+data['state']+" me gusta más..."}

        return {'message': "Post Not developed yet"}, 404

    def delete(self, id):
        return {'message': "Delete Not developed yet"}, 404

    def put(self, id):
        return {'message': "Put Not developed yet"}, 404
