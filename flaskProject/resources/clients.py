from flask_restful import Resource


class Clients(Resource):
    def get(self, id):
        return {'message': "Get Not developed yet"}, 404

    def post(self, id):
        return {'message': "Post Not developed yet"}, 404

    def delete(self, id):
        return {'message': "Delete Not developed yet"}, 404

    def put(self, id):
        return {'message': "Put Not developed yet"}, 404