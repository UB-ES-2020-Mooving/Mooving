from db import db
from models.constantes import generos

relations_table = db.Table('relations_table',
                           db.Column('clients', db.Integer, db.ForeignKey('clients.client_id')),
                           db.Column('motos', db.Integer, db.ForeignKey('motos.id'))
                           )

class ClientModel(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(9),nullable=False,unique=True)
    nombre = db.Column(db.String(50),nullable=False)
    genero = db.Column(db.Enum(*generos),nullable=False)

    motos = db.relationship('MotoModel',secondary=relations_table,
                                backref=db.backref('clients', lazy = 'dynamic'))

    def __init__(self, nombre, genero,dni):
        self.nombre = nombre
        self.genero = genero
        self.dni    = dni