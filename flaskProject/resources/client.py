from flask_restful import Resource, reqparse
from models.client_model import ClientModel
from models.reserved_running_model import ReservedRunningModel
from models.moto_model import MotoModel


class Client(Resource):
    def get(self, client_id):
        c = ClientModel.query.filter_by(client_id=client_id).first()
        if c:
            return {'client': c.json()}, 200
        else:
            return {'message': 'There is no client with ID [{}] .'.format(client_id)}, 404

    def post(self, client_id = None):

        #Creamos el request parser, que nos ayudará a manejar la informacion de entrada
        parser = reqparse.RequestParser()
        #Definimos que esperamos como entrada
        parser.add_argument('nombre', type=str,required=True, help="Name field cannot be left blanck")
        parser.add_argument('email', type=str,required=True, help="Email field cannot be left blanck")
        parser.add_argument('iban', type=str,required=True, help="IBAN field cannot be left blanck")
        parser.add_argument('dni_nie', type=str,required=True, help="DNI/NIE field cannot be left blanck")
        parser.add_argument('password', type=str, required=True, help="Password field cannot be left blanck")
        #Tomamos la información del parser en un diccionario (data)
        data = parser.parse_args()

        c = ClientModel.query.filter_by(email=data['email']).first()
        if c:
            return {'message': 'A client with same email [{}] already exists'.format(data['email'])}, 409

        c = ClientModel.query.filter_by(dni_nie=data['dni_nie']).first()
        if c:
            return {'message': 'A client with same DNI/NIE [{}] already exists'.format(data['dni_nie'])}, 409

        entry = ClientModel(data['nombre'],data['iban'],data['dni_nie'],data['email'],data['password'])
        entry.save_to_db()

        return entry.json(), 201

    def delete(self, email_client):

        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True, help="Password cannot be left blanck")
        data = parser.parse_args()

        password = data['password']
        c = ClientModel.find_by_email(email_client)
        if c: # Si existe el cliente
            if c.password == password: # Si la password coincide con la del cliente
                rr = ReservedRunningModel.find_by_client(c.client_id)
                if(rr is not None): # Si existe una reserva o start afiliada al cliente, indagamos
                    moto = MotoModel.find_by_id(rr.moto.id)
                    if(moto.state == "RESERVED"): # Si la moto esta reservada
                        # Borramos la fila de rr
                        rr.delete_from_db()
                        # Actualizamos el estado de la moto
                        moto.state = "AVAILABLE"
                        moto.save_to_db()
                        # Borramos el cliente
                        c.delete_from_db()
                        return {"message": "Client DELETED successfully"}, 200
                    if(moto.state == "ACTIVE"): # No podemos borrar el cliente porque antes tiene que finalizar el trayecto
                        return {'message': 'The account cannot be deleted because you have a journey started'}, 401
                else: # Si no existe reserva o start, podemos borrarlo directamente
                    c.delete_from_db()
                    return {"message": "Client DELETED successfully"}, 200
            else: # Password erronea
                return {'message': 'ERROR: The password is not correct.'}, 400
        else: # Si no existe el cliente
            return {'message': 'ERROR: There is no client with email [{}] .'.format(email_client)}, 404

    def put(self, client_id):
        # Creamos el request parser, que nos ayudará a manejar la informacion de entrada
        parser = reqparse.RequestParser()
        # Definimos que esperamos como entrada
        parser.add_argument('nombre', type=str, required=True, help="Name field cannot be left blanck")
        parser.add_argument('email', type=str, required=True, help="Email field cannot be left blanck")
        parser.add_argument('iban', type=str, required=True, help="IBAN field cannot be left blanck")
        # Tomamos la información del parser en un diccionario (data)
        data = parser.parse_args()

        c = ClientModel.query.filter_by(client_id=client_id).first()
        if c:
            c.nombre = data['nombre']
            c.email = data['email']
            c.iban = data['iban']
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


class Profile(Resource):
    def get(self, email):
        try:
            client = ClientModel.find_by_email(email)
            return {'client_profile': client.json_profile()}, 200
        except:
            return {"message": "Error Get Client Pofile"}, 500

    def put(self, email):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('iban', type=str, required=False)
        parser.add_argument('dni_nie', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        data = parser.parse_args()

        try:
            client = ClientModel.find_by_email(email)
            if(client is not None):
                if data['name']:
                    client.set_name(data['name'])
                if data['iban']:
                    client.set_iban(data['iban'])
                if data['dni_nie']:
                    client.set_dni_nie(data['dni_nie'])
                if data['email']:
                    client.set_email(data['email'])

                return {"message": "Client profile modified successfully"}, 200
            else:
                return {"message": "Client with this email doesn't exist"}, 404
        except:
            return {"message": "Error Modify client profile"}, 500


