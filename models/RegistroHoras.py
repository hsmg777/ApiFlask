from db import db
from datetime import date, time

class RegistroHoras(db.Model):
    __tablename__ = 'registroHoras'
    
    id_registroHoras = db.Column(db.Integer, primary_key=True)
    id_User = db.Column(db.Integer, db.ForeignKey('Usuario.id_User'), nullable=False)
    fecha = db.Column(db.Date, default=date.today)
    horaIngreso = db.Column(db.Time, nullable=False)
    horaSalida = db.Column(db.Time, nullable=True)
    horasLaboradas = db.Column(db.Time, nullable=True)

    # Relación con Usuario
    usuario = db.relationship('Usuario', backref='registro_horas', lazy=True)

    def __init__(self, id_User, fecha, horaIngreso, horaSalida=None, horasLaboradas=None):
        self.id_User = id_User
        self.fecha = fecha
        self.horaIngreso = horaIngreso
        self.horaSalida = horaSalida
        self.horasLaboradas = horasLaboradas
