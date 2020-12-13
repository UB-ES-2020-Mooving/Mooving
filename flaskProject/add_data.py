from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

from models.article_model import ArticleModel
from models.moto_model import MotoModel
from models.client_model import ClientModel
from models.mechanic_model import MechanicModel
from models.reserved_running_model import ReservedRunningModel

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
        state="AVAILABLE",
        matricula="1111-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=41.403193,
        last_coordinate_longitude=2.175004,
        km_restantes=34.0,
        km_totales=300.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto1)

    new_moto2 = MotoModel(
        state="AVAILABLE",
        matricula="2222-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=41.403719,
        last_coordinate_longitude=2.189128,
        km_restantes=3.0,
        km_totales=23.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto2)

    new_moto3 = MotoModel(
        state="AVAILABLE",
        matricula="3333-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=41.386399,
        last_coordinate_longitude=2.164143,
        km_restantes=120.0,
        km_totales=500.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto3)

    new_moto = MotoModel(
        state="AVAILABLE",
        matricula="4444-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=41.348788,
        last_coordinate_longitude=2.132925,
        km_restantes=45.0,
        km_totales=203.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto)

    new_moto = MotoModel(
        state="LOW_BATTERY_FUEL",
        matricula="5555-MMM",
        date_estreno="08/10/2020",
        model_generic="premium",
        last_coordinate_latitude=41.413273,
        last_coordinate_longitude=2.152931,
        km_restantes=2.0,
        km_totales=100.0,
        date_last_check="18/10/2020",
        km_last_check=100.0)
    db.session.add(new_moto)

    new_moto = MotoModel(
        state="LOW_BATTERY_FUEL",
        matricula="6666-MMM",
        date_estreno="08/10/2020",
        model_generic="premium",
        last_coordinate_latitude=41.427691,
        last_coordinate_longitude=2.166293,
        km_restantes=4.0,
        km_totales=100.0,
        date_last_check="18/10/2020",
        km_last_check=100.0)
    db.session.add(new_moto)

    new_moto = MotoModel(
        state="AVAILABLE",
        matricula="7777-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=41.387818,
        last_coordinate_longitude=2.169647,
        km_restantes=23.0,
        km_totales=203.0,
        date_last_check="18/10/2020",
        km_last_check=0.0)
    db.session.add(new_moto)

    new_moto = MotoModel(
        state="AVAILABLE",
        matricula="8888-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=41.375960,
        last_coordinate_longitude=2.177455,
        km_restantes=35.0,
        km_totales=203.0,
        date_last_check="18/10/2020",
        km_last_check=100.0)
    db.session.add(new_moto)

    client1 = ClientModel(
        nombre = "Juana",
        iban = "2223462362665251w",
        dni_nie = "11111111J",
        email = "juanita@gmail.com",
        password = "123456"
    )
    db.session.add(client1)

    client2 = ClientModel(
        nombre="Camila",
        iban="22462362665251w",
        dni_nie="14441111J",
        email="camila@gmail.com",
        password="123456"

    )
    db.session.add(client2)

    client3 = ClientModel(
        nombre="Sofia",
        iban="2223332362665251w",
        dni_nie="11188881J",
        email="sofia@gmail.com",
        password="123456"
    )
    db.session.add(client3)

    client = ClientModel(
        nombre="Ramona",
        iban="225554362665251w",
        dni_nie="12341111J",
        email="ramona@gmail.com",
        password="123456"
    )
    db.session.add(client)

    articulo=ArticleModel(
        titulo = "¡Motos más nuevas y potentes que nunca!",
        texto = "Las nuevas motos de Mooving están batiendo todos los"
                "récord habidos y por haber. Tenemos más de 400 motos eléctricas"
                "con una autonomía de más de 100KM.",
        fecha_creacion = "2020/10/29",
        visible = True)
    db.session.add(articulo)

    articulo=ArticleModel(
        titulo = "¡Motos más rápidas !",
        texto = "Las nuevas motos de Mooving son más rápidas que las de la competencia."
                " Tenemos más de 400 motos eléctricas"
                " con una velocidad punta de más de 100KM/H .",
        fecha_creacion = "2020/10/28",
        visible = True)
    db.session.add(articulo)

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


