from marshmallow import Schema, fields

class PlatoSchema(Schema):
    id_plato = fields.Int(dump_only=True)
    id_User = fields.Int(required=True)
    nombre = fields.Str(required=True)
    precio = fields.Float(required=True)
    descripcion = fields.Str()
    urlImg = fields.Str()
