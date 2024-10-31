from marshmallow import Schema, fields

class RegistroHorasSchema(Schema):
    id_registroHoras = fields.Int(dump_only=True)
    id_User = fields.Int(required=True)
    fecha = fields.Date(required=True)
    horaIngreso = fields.Time(required=True)
    horaSalida = fields.Time()
    horasLaboradas = fields.Time()
