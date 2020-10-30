
from flask_restful import Resource, reqparse
from models.client_model import ClientModel


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        try:
            client = ClientModel.find_by_email(data['email'])
            if client:
                if client.verify_password(data['password']):
                    return {'message': "Login succesfull",
                            'client': client.json()}, 200
                else:
                    return {"message": "Wrong password"}, 400
            else:
                return {"message": "User not found"}, 404
        except:
            return {"message": "Error Post Login"}, 500
