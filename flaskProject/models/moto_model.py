from db import db
from models.constantes import *
from datetime import datetime
from geopy.distance import distance

from sqlalchemy import and_, or_

from geopy.geocoders import Nominatim


class MotoModel(db.Model):
    __tablename__ = 'motos'

    # Atributo ID
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Atributo estado de la moto
    state = db.Column(db.Enum(*states_moto, name='states_types'), nullable=False)
    # Atributo matricula de la moto
    matricula = db.Column(db.String(30), nullable=False, unique=True)
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
    # Atributo address, direccion de la ultima aparcamiento de la moto
    address = db.Column(db.String(150),nullable=False)

    # Atributo km_restantes de la moto para que se le acabe la bateria
    km_restantes = db.Column(db.Float, nullable=False)
    # Atributo km_totales de la moto
    km_totales = db.Column(db.Float, nullable=False)
    # Atributo fecha ultima revision
    date_last_check = db.Column(db.String(30), nullable=False)
    # Atributo km recorrido en ultima revision (para los nuevos seran 0km)
    km_last_check = db.Column(db.Float, nullable=False)

    def __init__(self, state, matricula, date_estreno, model_generic, last_coordinate_latitude,
                 last_coordinate_longitude, km_restantes, km_totales, date_last_check, km_last_check):
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
        self.address = self.obtainAddressFromCoordinates(last_coordinate_latitude,last_coordinate_longitude)
        self.km_restantes = km_restantes
        self.km_totales = km_totales
        self.date_last_check = date_last_check
        self.km_last_check = km_last_check

    def obtainAddressFromCoordinates(self, last_coordinate_latitude,last_coordinate_longitude):
        geolocator = Nominatim(user_agent = "Mooving")
        location = geolocator.reverse(str(last_coordinate_latitude) + ',' + str(last_coordinate_longitude),
                                      language="es")
        return location.address

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
            'address': self.address,
            'km_restantes': self.km_restantes,
            'km_totales': self.km_totales,
            'date_last_check': self.date_last_check,
            'km_last_check': self.km_last_check,
        }
        return data

    def json_clientMoto(self):
        data = {
            'id': self.id,
            'matricula': self.matricula,
            'model_generic': self.model_generic,
            'km_restantes': self.km_restantes,
            'address': self.address,
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude,
        }
        return data

    def json_listmotos(self):
        data = {
            'id': self.id,
            'matricula': self.matricula,
            'model_generic': self.model_generic,
            'km_restantes': self.km_restantes,
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude,
        }
        return data



    def json_mechaniclistmotos(self):
        date_format = "%d/%m/%Y"
        date_last_check = datetime.strptime(self.date_last_check, date_format)
        today = datetime.strptime(datetime.now().strftime(date_format), date_format)
        time_since_last_check = (today - date_last_check).days

        date_estreno = datetime.strptime(self.date_estreno, date_format)
        time_total = (today - date_estreno).days

        data = {
            'license_plate': self.matricula,
            'state': self.state,
            'type': self.model_generic, #type of moto (basic, premium)
            'km_total': self.km_totales, #km since added to the system
            'time_total': time_total, #days since added to the system: date_estreno - date_actual
            'id': self.id,
            'time_since_last_check': time_since_last_check , #days since last check
            'km_since_last_check': self.km_totales - self.km_last_check , #km since last check
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude,
        }
        return data

    def json_mechanicMoto(self):
        date_format = "%d/%m/%Y"
        date_last_check = datetime.strptime(self.date_last_check, date_format)
        today = datetime.strptime(datetime.now().strftime(date_format), date_format)
        time_since_last_check = (today - date_last_check).days

        date_estreno = datetime.strptime(self.date_estreno, date_format)
        time_total = (today - date_estreno).days

        data = {
            'id': self.id,
            'matricula': self.matricula,
            'state': self.state,
            'type': self.model_generic,
            'km_total': self.km_totales,  # km since added to the system
            'time_total': time_total,  # days since added to the system: date_estreno - date_actual
            'time_since_last_check': time_since_last_check,  # days since last check
            'km_since_last_check': self.km_totales - self.km_last_check,  # km since last check
            'km_restantes': self.km_restantes,
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude,
            'address': self.address
        }
        return data


    def get_last_coordinate_latitude(self):
        return self.last_coordinate_latitude

    def get_last_coordinate_longitude(self):
        return self.last_coordinate_longitude

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_moto(self, state, matricula, date_estreno, model_generic, last_coordinate_latitude,
                 last_coordinate_longitude, km_restantes, km_totales, date_last_check,km_last_check):
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
        self.address = self.obtainAddressFromCoordinates(last_coordinate_latitude,last_coordinate_longitude)
        self.km_restantes = km_restantes
        self.km_totales = km_totales
        self.date_last_check = date_last_check
        self.km_last_check = km_last_check

    @classmethod
    def find_by_id(cls, id):
        return MotoModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_state(cls, state):
        return MotoModel.query.filter_by(state=state).all()

    @classmethod
    def get_all(cls):
        return MotoModel.query.all()

    @classmethod
    def compute_distance(cls, motos, coord, key_name, max_dist=float("inf")):
        # Este bloque es para comprobar que la key_name no coincida con otra key del diccionario y falle.
        if len(motos) > 0:
            json = motos[0]
            if key_name in json.keys():
                raise NameError('key_name ERROR. key_name cannot be the same as other keys'
                                'in the JSON.')
        # Valor al que se redondea la distancia
        round_value = 1
        data = {'motos': []}
        for m in motos:
            distancia_metros = distance((m['last_coordinate_latitude'], m['last_coordinate_latitude']), coord).m
            m[key_name] = round(distancia_metros / round_value) * round_value
            # Si es menor que la máxima distancia lo metemos
            if m[key_name] < max_dist:
                data['motos'].append(m)

        data['motos'].sort(key=lambda x: x[key_name])

        return data

    @classmethod
    def condiciones_AND(cls, lista):
        cond = and_()
        for c in lista:
            cond = and_(cond, c)
        return cond

