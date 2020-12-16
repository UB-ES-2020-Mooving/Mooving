from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from db import db

from flask_cors import CORS
from flask import render_template

from resources.article import ArticlesList
from resources.mechanic import Mechanic, MechanicList

from resources.client import Client, ClientsList, Profile
from resources.motos import Moto, ClientMotosList, MechanicMotosList, ClientMoto, MechanicMoto
from resources.login import Login
from resources.reserved_start import Reserved, Start
from resources.moto_error import MotoError

# App configuration
from decouple import config
app = Flask(__name__)
# Production configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='localhost')
# Developer configuration
if not config('PRODUCTION', cast=bool, default=False):
    # by default use this config if it's not in production env
    app.template_folder = '../frontend/dist'
    app.static_folder = '../frontend/dist/static'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# set db
api = Api(app)
CORS(app, resources={r'/*': {'origins':'*'}})
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

api.add_resource(ArticlesList, "/articles")

api.add_resource(Client, "/client/<int:client_id>", "/client", "/client/<string:email_client>")
api.add_resource(Profile, "/profile/<string:email>")
api.add_resource(ClientsList, '/clients')

api.add_resource(Moto, "/moto/<int:id>", "/moto")
api.add_resource(ClientMotosList, '/motos')
api.add_resource(MechanicMotosList, '/mechanicMotos')

api.add_resource(ClientMoto,'/clientMoto/<int:id>') # Para mostrar al cliente informacion de un moto en concreto
api.add_resource(MechanicMoto,'/mechanicMoto/<int:id>') # Para mostrar al mechanic informacion de un moto en concreto


api.add_resource(Login, '/login')

api.add_resource(Mechanic, "/mechanic/<int:id>", "/mechanic")
api.add_resource(MechanicList, '/mechanics')


api.add_resource(Reserved, "/reserve/<string:client_email>", "/reserve","/reserve/<string:client_email>/<int:moto_id>")
api.add_resource(Start, "/start/<string:client_email>", "/start", "/start/<string:client_email>/<int:moto_id>")


api.add_resource(MotoError, "/notifyError/<int:moto_id>")


@app.route('/')
def render_vue():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
