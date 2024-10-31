from db import db

class Usuario(db.Model):
    __tablename__ = 'Usuario'  # Doble guión bajo
    id_User = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Contrasenia = db.Column(db.String(50), nullable=False)
    Nombre = db.Column(db.String(30), nullable=False)
    Apellido = db.Column(db.String(30), nullable=False)
    Cedula = db.Column(db.Integer, nullable=False)
    Telefono = db.Column(db.String(20), nullable=False)
    isAdmin = db.Column(db.String(1), nullable=False, default='N')  # Nueva columna isAdmin con valor predeterminado 'N'

    def __init__(self, Username, Contrasenia, Nombre, Apellido, Cedula, Telefono, isAdmin='N'):
        self.Username = Username
        self.Contrasenia = Contrasenia
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Cedula = Cedula
        self.Telefono = Telefono
        self.isAdmin = isAdmin  # Inicializa isAdmin con el valor proporcionado o el valor predeterminado 'N'

    @classmethod
    def validar_credenciales(cls, username, contrasenia):
        """Valida si el usuario existe y la contraseña es correcta."""
        usuario = cls.query.filter_by(Username=username, Contrasenia=contrasenia).first()
        return usuario is not None
