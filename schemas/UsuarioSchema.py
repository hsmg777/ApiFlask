from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id_User = fields.Int(dump_only=True)
    Username = fields.Str(required=True)
    Contrasenia = fields.Str(required=True)  # Agregamos el campo de contraseña
    Nombre = fields.Str(required=True)
    Apellido = fields.Str(required=True)
    Cedula = fields.Int(required=True)
    Telefono = fields.Str(required=True)
