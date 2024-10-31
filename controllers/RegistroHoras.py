from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.RegistroHoras import RegistroHoras
from db import db
from schemas.RegistroHorasSchema import RegistroHorasSchema
from marshmallow import ValidationError
from datetime import datetime, timedelta

blp = Blueprint("RegistroHoras", __name__, url_prefix="/api/registrohoras", description="CRUD Registro de Horas")

registro_horas_schema = RegistroHorasSchema()
registros_horas_schema = RegistroHorasSchema(many=True)

@blp.route('/')
class RegistroHorasList(MethodView):
    @blp.response(200, RegistroHorasSchema(many=True))
    def get(self):
        """Obtener todos los registros de horas"""
        try:
            registros = RegistroHoras.query.all()
            return registros
        except Exception as e:
            print(f"Error al obtener registros de horas: {e}")
            abort(500, message="Error al obtener registros de horas")

    @blp.arguments(RegistroHorasSchema)
    @blp.response(201, RegistroHorasSchema)
    def post(self, data):
        """Crear un nuevo registro de horas"""
        try:
            nuevo_registro = RegistroHoras(
                id_User=data['id_User'],
                fecha=data['fecha'],
                horaIngreso=data['horaIngreso'],
                horaSalida=data.get('horaSalida'),
                horasLaboradas=data.get('horasLaboradas')
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            print("Registro de horas creado con éxito:", nuevo_registro.id_registroHoras)
            return nuevo_registro
        except Exception as e:
            print(f"Error al crear registro de horas: {e}")
            abort(500, message="Error al crear registro de horas")


@blp.route('/<int:id_registroHoras>')
class RegistroHorasResource(MethodView):
    @blp.response(200, RegistroHorasSchema)
    def get(self, id_registroHoras):
        """Obtener un registro de horas por ID"""
        registro = RegistroHoras.query.get(id_registroHoras)
        if registro is None:
            abort(404, message="Registro de horas no encontrado")
        return registro

    @blp.arguments(RegistroHorasSchema)
    @blp.response(200, RegistroHorasSchema)
    def put(self, data, id_registroHoras):
        """Actualizar un registro de horas"""
        registro = RegistroHoras.query.get(id_registroHoras)
        if registro is None:
            abort(404, message="Registro de horas no encontrado")

        # Actualiza los campos
        registro.id_User = data['id_User']
        registro.fecha = data['fecha']
        registro.horaIngreso = data['horaIngreso']
        registro.horaSalida = data.get('horaSalida')
        
        # Calcular horas laboradas si se proporcionan hora de ingreso y salida
        if registro.horaIngreso and registro.horaSalida:
            hora_ingreso = datetime.combine(registro.fecha, registro.horaIngreso)
            hora_salida = datetime.combine(registro.fecha, registro.horaSalida)
            horas_laboradas = hora_salida - hora_ingreso
            registro.horasLaboradas = (datetime.min + horas_laboradas).time()

        db.session.commit()
        print("Registro de horas actualizado con éxito:", registro.id_registroHoras)
        return registro

    @blp.response(204)
    def delete(self, id_registroHoras):
        """Eliminar un registro de horas"""
        registro = RegistroHoras.query.get(id_registroHoras)
        if registro is None:
            abort(404, message="Registro de horas no encontrado")
        
        db.session.delete(registro)
        db.session.commit()
        print("Registro de horas eliminado con éxito:", id_registroHoras)
        return '', 204
