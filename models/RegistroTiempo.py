from db import db
from datetime import date, time

class RegistroTiempo(db.Model):
    __tablename__ = 'registroTiempo'

    id_registroTiempo = db.Column(db.Integer, primary_key=True)
    id_User = db.Column(db.Integer, db.ForeignKey('Usuario.id_User'), nullable=False)
    id_plato = db.Column(db.Integer, db.ForeignKey('Plato.id_plato'), nullable=True)  
    fecha = db.Column(db.Date, default=date.today, nullable=False)
    tiempoInicio = db.Column(db.Time, nullable=False)
    tiempoFin = db.Column(db.Time, nullable=True)
    tiempoTotal = db.Column(db.Time, nullable=True)

    usuario = db.relationship('Usuario', backref='registro_horas', lazy=True)
    plato = db.relationship('Plato', backref='registro_tiempo', lazy=True)

    def __init__(self, id_User, id_plato=None, fecha=None, tiempoInicio=None, tiempoFin=None, tiempoTotal=None):
        self.id_User = id_User
        self.id_plato = id_plato
        self.fecha = fecha or date.today()
        self.tiempoInicio = tiempoInicio
        self.tiempoFin = tiempoFin
        self.tiempoTotal = tiempoTotal
