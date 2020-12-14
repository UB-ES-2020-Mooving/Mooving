from flask_restful import Resource, reqparse

from models.moto_model import MotoModel
from models.reserved_running_model import ReservedRunningModel


class MotoError(Resource):
    def post(self, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            if moto is not None:
                if moto.state == "RESERVED" or moto.state == "ACTIVE":
                    rr = ReservedRunningModel.find_by_moto(moto.id)
                    rr.delete_from_db()
                    moto.set_state("ALERT")
                    return {"message": "Correctly reported error"}, 200
                else:
                    moto.set_state("ALERT")
                    return {"message": "Correctly reported error"}, 200
            else:
                return {"message": "Moto not found"}, 404
        except:
            return {"message": "Internal error when reporting the error"}, 500

