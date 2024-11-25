from marshmallow import Schema, fields

class RegistroTiempoSchema(Schema):
    id_registroTiempo = fields.Int(dump_only=True)  
    id_User = fields.Int(required=True)  
    id_plato = fields.Int(allow_none=True)  
    fecha = fields.Date(required=True)  
    tiempoInicio = fields.Time(required=True) 
    tiempoFin = fields.Time(allow_none=True) 
    tiempoTotal = fields.Time(allow_none=True) 

