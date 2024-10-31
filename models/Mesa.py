from db import db

class Mesa(db.Model):
    __tablename__ = 'Mesa'
    
    id_mesa = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre
