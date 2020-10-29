from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.moto_model import MotoModel
from models.client_model import ClientModel
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


def init_db():
    db.drop_all()
    db.create_all()
    new_moto1 = MotoModel(
        state="ACTIVE",
        matricula="1111-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=23.4433,
        last_coordinate_longitude=23.4433,
        km_restantes=80.0,
        km_totales=0.0,
        date_last_check="18/10/2020")
    db.session.add(new_moto1)

    new_moto2 = MotoModel(
        state="ACTIVE",
        matricula="2222-MMM",
        date_estreno="28/10/2020",
        model_generic="basic",
        last_coordinate_latitude=23.4433,
        last_coordinate_longitude=23.4433,
        km_restantes=80.0,
        km_totales=0.0,
        date_last_check="18/10/2020")
    db.session.add(new_moto2)

    new_moto3 = MotoModel(
        state="ACTIVE",
        matricula="3333-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4433,
        last_coordinate_longitude=23.4433,
        km_restantes=120.0,
        km_totales=0.0,
        date_last_check="18/10/2020")
    db.session.add(new_moto3)

    new_moto4 = MotoModel(
        state="ACTIVE",
        matricula="4444-MMM",
        date_estreno="28/10/2020",
        model_generic="premium",
        last_coordinate_latitude=23.4433,
        last_coordinate_longitude=23.4433,
        km_restantes=120.0,
        km_totales=0.0,
        date_last_check="18/10/2020")
    db.session.add(new_moto4)

    client1 = ClientModel(
        nombre = "Juana",
        genero = "mujer",
        iban = "2223462362665251w",
        dni_nie = "11111111J",
        email = "juanita@gmail.com",
        password = "1234"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Camila",
        genero="mujer",
        iban="22462362665251w",
        dni_nie="14441111J",
        email="Camila@gmail.com",
        password="1234"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Sofia",
        genero="mujer",
        iban="2223332362665251w",
        dni_nie="11188881J",
        email="Sofia@gmail.com",
        password="1234"
    )
    db.session.add(client1)

    client1 = ClientModel(
        nombre="Ramona",
        genero="mujer",
        iban="225554362665251w",
        dni_nie="12341111J",
        email="Ramona@gmail.com",
        password="1234"
    )
    db.session.add(client1)


    """
    client1 = ClientModel(
        nombre = ,
        genero = ,
        iban = ,
        dni_nie = ,
        email = ,
        password = 
    )"""


    db.session.commit()
