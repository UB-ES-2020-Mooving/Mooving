from flask_restful import Resource, reqparse

from models.moto_model import MotoModel
from models.reserved_running_model import ReservedRunningModel


class MotoError(Resource):
    def post(self, moto_id):
        try:
            moto = MotoModel.find_by_id(moto_id)
            if(moto is not None):
                ReservedRunningModel.find_by_moto(moto_id)
                moto.set_state("ALERT")
            else:
                return {"message": "Moto not found"}, 404

        except:
            return {"message": "Internal error when reporting the error"}, 500