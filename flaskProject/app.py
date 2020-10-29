from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from db import db

from models.moto_model import MotoModel
from models.client_model import ClientModel
from resources.article import ArticlesList

from resources.client import Client, ClientsList
from resources.motos import Moto, MotosList


app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)



"""
Para volver a crear la base de datos:
    1. borrar la carpeta migrations y el archivo data.db
    
    (Antes de ejecutar el segundo asegurarnos que las líneas del 3.
    están comentadas.)
    2. abrir terminal y escribir:
        flask db init
        flask db migrate -m "Initial migration."
        flask db upgrade
    3.Descomentamos las dos lineas siguientes :
        (
        from add_data import init_db
        init_db()
        )
        y ejecutamos app.py
    4.volvemos a comentar las lineas que acabamos de descomentar.
"""
#from add_data import init_db
#init_db()

api.add_resource(ArticlesList,"/articles")

api.add_resource(Client, "/client/<int:client_id>", "/client")
api.add_resource(ClientsList, '/clients')

api.add_resource(Moto,"/moto/<int:id>","/moto")
api.add_resource(MotosList, '/motos')



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
