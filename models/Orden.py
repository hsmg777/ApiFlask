from db import db
from datetime import date

class Orden(db.Model):
    __tablename__ = 'Orden'
    
    id_orden = db.Column(db.Integer, primary_key=True)
    id_plato = db.Column(db.Integer, db.ForeignKey('Plato.id_plato'), nullable=False)
    id_mesa = db.Column(db.Integer, db.ForeignKey('Mesa.id_mesa'), nullable=False)
    fecha = db.Column(db.Date, default=date.today)
    cantidad = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.String(200), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")  
    
    # Relaciones con Plato y Mesa
    plato = db.relationship('Plato', backref='ordenes', lazy=True)
    mesa = db.relationship('Mesa', backref='ordenes', lazy=True)

    def __init__(self, id_plato, id_mesa, cantidad, observacion=None, estado="Pendiente"):
        self.id_plato = id_plato
        self.id_mesa = id_mesa
        self.fecha = date.today()
        self.cantidad = cantidad
        self.observacion = observacion
        self.estado = estado
