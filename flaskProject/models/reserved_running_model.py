from db import db
from datetime import datetime, timedelta


class ReservedRunningModel(db.Model):
    __tablename__ = 'reserved_running'

    rr_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Atributo relacion con la tabla clients
    clientId = db.Column(db.String(50), db.ForeignKey('clients.client_id'), unique=True)
    # Atributo relacion con la tabla motos
    motoId = db.Column(db.Integer, db.ForeignKey('motos.id'), unique=True)

    # Atributo fecha y hora de la reserva. Formato DD/MM/YYYY HH:MM:SS
    dateTimeReserved = db.Column(db.DATETIME)
    # Atributo fecha y hora del running(start). Formato DD/MM/YYYY HH:MM:SS
    dateTimeStart = db.Column(db.DATETIME)
    # Atributo kilometros de la moto antes de hacer el start
    kmStart = db.Column(db.Float)

    def __init__(self, client, moto):
        self.client = client
        self.moto = moto
        self.dateTimeReserved = datetime.now()
        self.kmStart = moto.km_totales

    def json_reserved(self):
        data = {
            'id': self.rr_id,
            'client': self.client.json(),
            'moto': self.moto.json(),
            'dataTimeReserved': self.convert_date_to_string(self.dateTimeReserved),
            'kmStart': self.kmStart
        }
        return data

    def json_start(self):
        data = {
            'id': self.rr_id,
            'client': self.client.json(),
            'moto': self.moto.json(),
            'dataTimeReserved': self.convert_date_to_string(self.dateTimeReserved),
            'dataTimeStart': self.convert_date_to_string(self.dateTimeStart),
            'kmStart': self.kmStart
        }
        return data

    def json_prueba(self):
        data = {
            'id': self.id,
            'matricula': self.matricula,
            'model_generic': self.model_generic,
            'km_restantes': self.km_restantes,
            'address': self.address,
            'last_coordinate_latitude': self.last_coordinate_latitude,
            'last_coordinate_longitude': self.last_coordinate_longitude
        }
        return data


    def convert_date_to_string(self, dateTime):
        """
        Metodo que permite convertir el formato DateTime en formato String
        """
        data_time = str(dateTime.day) + "/" \
                    + str(dateTime.month) + "/" \
                    + str(dateTime.year) + " " \
                    + str(dateTime.hour) + ":" \
                    + str(dateTime.minute) + ":" \
                    + str(dateTime.second)
        return data_time

    def make_star_moto(self):
        """
        Metodo que permite hacer el put de star en reserved
        """
        self.dateTimeStart = datetime.now()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return ReservedRunningModel.query.filter_by(rr_id=id).first()

    @classmethod
    def find_by_client(cls, client_id):
        return ReservedRunningModel.query.filter_by(clientId=client_id).first()

    @classmethod
    def find_by_client_moto(cls, client_id, moto_id):
        return ReservedRunningModel.query.filter_by(clientId=client_id).filter_by(motoId=moto_id).first()

    def update_state_reserved(self):
        """
        Metodo que permite actualizar el estado de la moto y ponerlo a 'RESERVED'
        """
        self.moto.set_state('RESERVED')
        db.session.commit()

    def update_state_start(self):
        """
        Metodo que permite actualizar el estado de la moto y ponerlo a 'ACTIVE'
        """
        self.moto.set_state('ACTIVE')
        db.session.commit()

    def isReserved(self):
        return self.moto.state == "RESERVED"

    def isActive(self):
        return self.moto.state == "ACTIVE"

    def make_remaining_time(self):
        """
        Metodo que permite crear el tiempo limite para start moto desde la reserva
        """

        """
        Codigo real para la web
        time_min = 10

        ten_min_more = self.dateTimeReserved + timedelta(minutes=time_min)

        return mas10min
        """

        # Este tiempo es solo para la demo
        time_sg = 30

        mas10min = self.dateTimeReserved + timedelta(seconds=time_sg)

        return mas10min

    def check_remaining_time(self):
        """
        Metodo que permite comprobar si no se ha superado el tiempo limite para start moto (True) o si se ha superado (False)
        """
        # Si el tiempo reservado es menor al tiempo limite
        return datetime.now() <= self.make_remaining_time()

    def update_state_available(self):
        """
        Metodo que permite actualizar el estado de la moto y ponerlo a 'AVAILABLE'
        """
        self.moto.set_state('AVAILABLE')
        db.session.commit()