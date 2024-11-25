from marshmallow import Schema, fields

class LoginMesaSchema(Schema):
    nombre = fields.Str(required=True)
    passw = fields.Str(required=True)
