from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from data import clients, motos
from models.moto_model import MotoModel
from models.client_model import ClientModel

from resources.clients import Clients
from resources.motos import Motos

from db import db

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)





api.add_resource(Motos,"/motos/<int:id>","/motos")
#api.add_resource(Clients)




@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
