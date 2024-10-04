from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str(required=True)
    contrasenia = fields.Str(required=True)
