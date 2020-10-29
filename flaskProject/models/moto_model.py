from db import db
from models.constantes import *


class MotoModel(db.Model):
    __tablename__ = 'motos'

    # Atributo ID
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Atributo estado de la moto
    state = db.Column(db.Enum(*states_moto), nullable=False)
    # Atributo matricula de la moto
    matricula = db.Column(db.String(30), nullable=False)
    # Fecha estreno de la moto
    date_estreno = db.Column(db.String(30), nullable=False)

    # Atributo modelo generico de la moto en la empresa
    model_generic = db.Column(db.String(10), nullable=False)
    # Atributo modelo fabrica de la moto en la empresa
    model_fabric = db.Column(db.String(10), nullable=False)
    # Atributo cilindrada de la moto
    cc = db.Column(db.Integer, nullable=False)
    # Atributo autonomia de la bateria de la moto en KM
    battery_autonomy = db.Column(db.Integer, nullable=False)

    # Atributo last_coordinate_latitude, ultima coordenada latitud de la moto
    last_coordinate_latitude = db.Column(db.Float, nullable=False)
    # Atributo last_coordinate_longitude, ultima coordenada longitud de la moto
    last_coordinate_longitude = db.Column(db.Float, nullable=False)

    # Atributo km_restantes de la moto para que se le acabe la bateria
    km_restantes = db.Column(db.Float, nullable=False)
    # Atributo km_totales de la moto
    km_totales = db.Column(db.Float, nullable=False)
    # Atributo fecha ultima revision
    date_last_check = db.Column(db.String(30), nullable=False)

    def __init__(self, state, matricula, date_estreno, model_generic, last_coordinate_latitude,
                 last_coordinate_longitude, km_restantes, km_totales, date_last_check):
        self.state = state
        self.matricula = matricula
        self.date_estreno = date_estreno
        self.model_generic = model_generic
        if model_generic == "basic":
            self.model_fabric = moto_model_basic["model"]
            self.cc = moto_model_basic["cc"]
            self.battery_autonomy = moto_model_basic["battery_autonomy"]
        if model_generic == "premium":
            self.model_fabric = moto_model_premium["model"]
            self.cc = moto_model_premium["cc"]
            self.battery_autonomy = moto_model_premium["battery_autonomy"]
        self.last_coordinate_latitude = last_coordinate_latitude
        self.last_coordinate_longitude = last_coordinate_longitude
        self.km_restantes = km_restantes
        self.km_totales = km_totales
        self.date_last_check = date_last_check

    def json(self):
        data = {
            'id': self.id,
            'state': self.state,
            'matricula': self.matricula,
            'date_estreno': self.date_estreno,
            'model_generic': self.model_generic,
            'model_fabric': self.model_fabric,
            'cc': self.cc,
            'battery_autonomy': self.battery_autonomy,
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude,
            'km_restantes': self.km_restantes,
            'km_totales': self.km_totales,
            'date_last_check': self.date_last_check,
        }
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_moto(self, state, matricula, date_estreno, model_generic, last_coordinate_latitude,
                 last_coordinate_longitude, km_restantes, km_totales, date_last_check):
        self.state = state
        self.matricula = matricula
        self.date_estreno = date_estreno
        self.model_generic = model_generic
        if model_generic == "basic":
            self.model_fabric = moto_model_basic["model"]
            self.cc = moto_model_basic["cc"]
            self.battery_autonomy = moto_model_basic["battery_autonomy"]
        if model_generic == "premium":
            self.model_fabric = moto_model_premium["model"]
            self.cc = moto_model_premium["cc"]
            self.battery_autonomy = moto_model_premium["battery_autonomy"]
        self.last_coordinate_latitude = last_coordinate_latitude
        self.last_coordinate_longitude = last_coordinate_longitude
        self.km_restantes = km_restantes
        self.km_totales = km_totales
        self.date_last_check = date_last_check

    @classmethod
    def find_by_id(cls, id):
        return MotoModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_state(cls, state):
        return MotoModel.query.filter_by(state=state).all()

    @classmethod
    def get_all(cls):
        return MotoModel.query.all()

