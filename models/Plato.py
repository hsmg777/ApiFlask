from db import db

class Plato(db.Model):
    __tablename__ = 'Plato'
    
    id_plato = db.Column(db.Integer, primary_key=True)
    id_User = db.Column(db.Integer, db.ForeignKey('Usuario.id_User'), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))
    urlImg = db.Column(db.String, nullable=True)

    # Relación con Usuario
    usuario = db.relationship('Usuario', backref='platos', lazy=True)

    def __init__(self, id_User, nombre, precio, descripcion=None, urlImg=None):
        self.id_User = id_User
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.urlImg = urlImg
