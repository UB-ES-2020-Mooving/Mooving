from db import db


class MechanicModel(db.Model):

    __tablename__ = 'mechanics'

    # Atributo ID
    mechanic_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Name
    name = db.Column(db.String(30), nullable=False)
    # Subname
    subname = db.Column(db.String(30), nullable=False)
    # DNI
    dni = db.Column(db.String(20), nullable=False, unique=True)
    # Email
    email = db.Column(db.String(30))
    # Password
    password = db.Column(db.String(30), nullable=False)
    # Fecha de alta
    date_registration = db.Column(db.String(20), nullable=False)

    def __init__(self, name, subname, dni, password, date_registration):
        self.name = name
        self.subname = subname
        self.dni = dni
        self.email = self.make_email_mechanic(dni)
        self.password = password
        self.date_registration = date_registration

    def make_email_mechanic(self, dni):
        email = ''
        email += str(dni)
        email = email.lower()
        email += "@mooving.com"
        return email

    def json(self):
        return {
            "id": self.mechanic_id,
            "name": self.name,
            "subname": self.subname,
            "dni": self.dni,
            "email": self.email,
            "password": self.password,
            "date_registration": self.date_registration
        }

    def set_name(self, name):
        self.name = name
        db.session.commit()

    def set_subname(self, subname):
        self.subname = subname
        db.session.commit()

    def set_password(self, password):
        self.password = password
        db.session.commit()

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

    @classmethod
    def find_by_id(cls, mechanic_id):
        return MechanicModel.query.filter_by(mechanic_id=mechanic_id).first()

    @classmethod
    def find_by_email(cls, email):
        return MechanicModel.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls):
        return MechanicModel.query.all()

    # Metodo que comprueba si la contraseña es correcta
    def verify_password(self, password):
        return self.password.__eq__(password)

