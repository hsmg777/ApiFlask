from marshmallow import Schema, fields

class FechaRangoSchema(Schema):
    fecha_inicio = fields.Date(required=True, format='%Y-%m-%d', error_messages={
        "required": "La fecha de inicio es obligatoria",
        "invalid": "Formato inválido para la fecha de inicio, debe ser 'YYYY-MM-DD'"
    })
    fecha_fin = fields.Date(required=True, format='%Y-%m-%d', error_messages={
        "required": "La fecha de fin es obligatoria",
        "invalid": "Formato inválido para la fecha de fin, debe ser 'YYYY-MM-DD'"
    })
