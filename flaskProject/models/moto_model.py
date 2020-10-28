from db import db
from resources.motos import Motos
from models.constantes import estados


class MotoModel(db.Model):

    __tablename__ = 'motos'

    moto_id = db.Column(db.Integer, primary_key=True)

    estado = db.Column(db.Enum(*estados))
    km_totales = db.Column(db.Float,nullable=False)
    km_ultima_revision = db.Column(db.Float,nullable=False)
    #Para la fecha intentemos utilizar el formato AAAA/MM/DIA (10 caracteres)
    fecha_ultima_revision = db.Column(db.String(10))

    #También existe la variable    clients
    #Esto es asi por la relación many to many que hay definida en client.


    def __init__(self):
        self.estado = 'garage'
        self.km_totales = 0.
        self.km_ultima_revision = 0.
        self.fecha_ultima_revision = None