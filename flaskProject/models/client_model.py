from db import db
from models.constantes import generos

relations_table = db.Table('relations_table',
                           db.Column('clients', db.Integer, db.ForeignKey('clients.client_id')),
                           db.Column('motos', db.Integer, db.ForeignKey('motos.id'))
                           )


class ClientModel(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)

    # Personal
    nombre = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.Enum(*generos), nullable=False)

    # Bancario
    iban = db.Column(db.String(24), nullable=False)
    # Únicos
    dni_nie = db.Column(db.String(9), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)

    # Provisional
    password = db.Column(db.String(20), nullable=False)

    # Para la referencia many_to_many con la tabla de motos.
    motos = db.relationship('MotoModel', secondary=relations_table,
                            backref=db.backref('clients', lazy='dynamic'))

    def __init__(self, nombre, genero, iban, dni_nie, email, password):
        self.nombre = nombre
        self.email = email
        self.iban = iban
        self.password = password
        self.genero = genero
        self.dni_nie = dni_nie

    def json(self):
        return {"client":{
        "client_id":self.client_id,
        "nombre": self.nombre,
        "email" : self.email,
        "iban" : self.iban,
        "genero" : self.genero,
        "dni_nie" : self.dni_nie
        }}

    def save_to_db(self):
        """Saves instance to DB
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes instance from DB
        """
        db.session.delete(self)
        db.session.commit()
