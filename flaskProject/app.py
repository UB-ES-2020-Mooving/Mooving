from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from db import db

from models.moto_model import MotoModel
from models.client_model import ClientModel

from resources.clients import Clients
from resources.motos import Moto, MotosList


app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)



"""
Para volver a crear la base de datos:
    Primero borrar la carpeta migrations y el archivo data.db
    Segundo abrir terminal y escribir:
        - python3 -m flask db init
        - python3 -m flask db migrate -m "Initial migration."
        - python3 -m flask db upgrade
"""
#from add_data import init_db
#init_db()
api.add_resource(Clients, "/clients/<int:client_id>", "/clients")

api.add_resource(Moto,"/moto/<int:id>","/moto")
api.add_resource(MotosList, '/motos')



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
