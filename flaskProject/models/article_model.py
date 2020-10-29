from db import db

class ArticleModel(db.Model):

    __tablename__ = 'articles'

    article_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200),nullable=False)
    texto = db.Column(db.String(1000),nullable=False)
    # Para la fecha intentemos utilizar el formato AAAA/MM/DIA (10 caracteres)
    fecha_creacion = db.Column(db.String(10),nullable=False)
    visible = db.Column(db.Boolean,nullable=False)
    #También existe la variable    clients
    #Esto es asi por la relación many to many que hay definida en client.


    def __init__(self,titulo,texto,fecha_creacion,visible):
        self.titulo = titulo
        self.texto = texto
        self.fecha_creacion = fecha_creacion
        self.visible = visible

    def json(self):
        return {
        "titulo":self.titulo,
        "texto": self.texto,
        "fecha_creacion" : self.fecha_creacion,
        "visible" : self.visible,
        }

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