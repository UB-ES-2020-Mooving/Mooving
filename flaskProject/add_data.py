from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from models.article_model import ArticleModel
from models.moto_model import MotoModel
from models.client_model import ClientModel

from models.mechanic_model import MechanicModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if config('PRODUCTION', cast=bool, default=False):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='localhost')

db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()
    new_moto1 = MotoModel(
        state="ACTIVE",
        matricula="1111-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=23.4433,
        last_coordinate_longitude=23.4432,
        km_restantes=80.0,
        km_totales=0.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto1)

    new_moto2 = MotoModel(
        state="ACTIVE",
        matricula="2222-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=23.4431,
        last_coordinate_longitude=23.4433,
        km_restantes=80.0,
        km_totales=0.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto2)

    new_moto3 = MotoModel(
        state="ACTIVE",
        matricula="3333-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4434,
        last_coordinate_longitude=23.4433,
        km_restantes=120.0,
        km_totales=0.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto3)

    new_moto4 = MotoModel(
        state="ACTIVE",
        matricula="4444-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4431,
        last_coordinate_longitude=23.4432,
        km_restantes=120.0,
        km_totales=0.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto4)

    new_moto5 = MotoModel(
        state="LOW_BATTERY_FUEL",
        matricula="5555-MMM",
        date_estreno="08/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4434,
        last_coordinate_longitude=23.4431,
        km_restantes=30.0,
        km_totales=100.0,
        date_last_check="18/10/2020",
        km_last_check=100.0)
    db.session.add(new_moto5)

    new_moto6 = MotoModel(
        state="LOW_BATTERY_FUEL",
        matricula="6666-MMM",
        date_estreno="08/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4434,
        last_coordinate_longitude=23.4431,
        km_restantes=30.0,
        km_totales=100.0,
        date_last_check="18/10/2020",
        km_last_check=100.0)
    db.session.add(new_moto6)

    client1 = ClientModel(
        nombre = "Juana",
        iban = "2223462362665251w",
        dni_nie = "11111111J",
        email = "juanita@gmail.com",
        password = "123456"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Camila",
        iban="22462362665251w",
        dni_nie="14441111J",
        email="Camila@gmail.com",
        password="123456"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Sofia",
        iban="2223332362665251w",
        dni_nie="11188881J",
        email="Sofia@gmail.com",
        password="123456"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Ramona",
        iban="225554362665251w",
        dni_nie="12341111J",
        email="Ramona@gmail.com",
        password="123456"
    )
    db.session.add(client1)
    """
    client1 = ClientModel(
        nombre = ,
        iban = ,
        dni_nie = ,
        email = ,
        password = 
    )"""

    articulo1=ArticleModel(
        titulo = "¡Motos más nuevas y potentes que nunca!",
        texto = "Las nuevas motos de Mooving están batiendo todos los"
                "récord habidos y por haber. Tenemos más de 400 motos eléctricas"
                "con una autonomía de más de 100KM.",
        fecha_creacion = "2020/10/29",
        visible = True)
    db.session.add(articulo1)

    articulo1=ArticleModel(
        titulo = "¡Motos más rápidas !",
        texto = "Las nuevas motos de Mooving son más rápidas que las de la competencia."
                " Tenemos más de 400 motos eléctricas"
                " con una velocidad punta de más de 100KM/H .",
        fecha_creacion = "2020/10/28",
        visible = True)
    db.session.add(articulo1)

    new_mechanic = MechanicModel(
        name="Jose",
        subname="De carglass",
        dni="11111111J",
        password="123456",
        date_registration="23/02/2020")
    db.session.add(new_mechanic)

    new_mechanic = MechanicModel(
        name="Pepe",
        subname="De marcota",
        dni="22222222J",
        password="123456",
        date_registration="24/02/2020")
    db.session.add(new_mechanic)

    db.session.commit()
    print('Success in adding items to database')


#Si usa script --> deja la linea de abajo descomentada

init_db()

