from marshmallow import Schema, fields

class OrdenSchema(Schema):
    id_orden = fields.Int(dump_only=True)
    id_plato = fields.Int(required=True)
    id_mesa = fields.Int(required=True)
    fecha = fields.Date(dump_only=True)
    cantidad = fields.Int(required=True)
    observacion = fields.Str()
    estado = fields.Str(required=True)  
