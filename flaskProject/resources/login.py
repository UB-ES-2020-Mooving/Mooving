
from flask_restful import Resource, reqparse
from models.client_model import ClientModel
from models.mechanic_model import MechanicModel


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be left blank")
        data = parser.parse_args()

        try:
            email_aux = data['email'].split("@")
            print(email_aux)
            if "mooving.com" in email_aux:
                print("entramos mecanico")
                mechanic = MechanicModel.find_by_email(data['email'])
                if mechanic:
                    if mechanic.verify_password(data['password']):
                        return {'message': "Login succesfull",
                                'mechanic': mechanic.json(),
                                'type': "mechanic"}, 200
                    else:
                        return {"message": "Wrong password"}, 400
                else:
                    return {"message": "Mechanic not found"}, 404

            else:
                print("entramos cliente")
                client = ClientModel.find_by_email(data['email'])
                if client:
                    if client.verify_password(data['password']):
                        return {'message': "Login succesfull",
                                'client': client.json(),
                                'type': "client"}, 200
                    else:
                        return {"message": "Wrong password"}, 400
                else:
                    return {"message": "User not found"}, 404
        except:
            return {"message": "Error Post Login"}, 500
