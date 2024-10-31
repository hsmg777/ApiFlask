from marshmallow import Schema, fields

class MesaSchema(Schema):
    id_mesa = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
