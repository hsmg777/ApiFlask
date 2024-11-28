from marshmallow import Schema, fields

class PlatosChefSchema(Schema):
    idChef = fields.Int(required=True, error_messages={
        "required": "El campo 'idChef' es obligatorio",
        "invalid": "El 'idChef' debe ser un número entero"
    })
    fecha_inicio = fields.Date(required=True, format='%Y-%m-%d', error_messages={
        "required": "El campo 'fecha_inicio' es obligatorio",
        "invalid": "Formato inválido para 'fecha_inicio', debe ser 'YYYY-MM-DD'"
    })
    fecha_fin = fields.Date(required=True, format='%Y-%m-%d', error_messages={
        "required": "El campo 'fecha_fin' es obligatorio",
        "invalid": "Formato inválido para 'fecha_fin', debe ser 'YYYY-MM-DD'"
    })
