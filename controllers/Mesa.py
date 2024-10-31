from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Mesa import Mesa
from db import db
from schemas.MesaSchema import MesaSchema
from marshmallow import ValidationError

blp = Blueprint("Mesa", __name__, url_prefix="/api/mesa", description="CRUD Mesa")

mesa_schema = MesaSchema()
mesas_schema = MesaSchema(many=True)

@blp.route('/')
class MesaList(MethodView):
    @blp.response(200, MesaSchema(many=True))
    def get(self):
        """Obtener todas las mesas"""
        try:
            mesas = Mesa.query.all()
            return mesas
        except Exception as e:
            print(f"Error al obtener mesas: {e}")
            abort(500, message="Error al obtener mesas")

    @blp.arguments(MesaSchema)
    @blp.response(201, MesaSchema)
    def post(self, data):
        """Crear una nueva mesa"""
        try:
            nueva_mesa = Mesa(nombre=data['nombre'])
            db.session.add(nueva_mesa)
            db.session.commit()
            print("Mesa creada con éxito:", nueva_mesa.nombre)
            return nueva_mesa
        except Exception as e:
            print(f"Error al crear mesa: {e}")
            abort(500, message="Error al crear mesa")


@blp.route('/<int:id_mesa>')
class MesaResource(MethodView):
    @blp.response(200, MesaSchema)
    def get(self, id_mesa):
        """Obtener una mesa por ID"""
        mesa = Mesa.query.get(id_mesa)
        if mesa is None:
            abort(404, message="Mesa no encontrada")
        return mesa

    @blp.arguments(MesaSchema)
    @blp.response(200, MesaSchema)
    def put(self, data, id_mesa):
        """Actualizar una mesa"""
        mesa = Mesa.query.get(id_mesa)
        if mesa is None:
            abort(404, message="Mesa no encontrada")

        # Actualiza el campo
        mesa.nombre = data['nombre']
        db.session.commit()
        print("Mesa actualizada con éxito:", mesa.nombre)
        return mesa

    @blp.response(204)
    def delete(self, id_mesa):
        """Eliminar una mesa"""
        mesa = Mesa.query.get(id_mesa)
        if mesa is None:
            abort(404, message="Mesa no encontrada")
        
        db.session.delete(mesa)
        db.session.commit()
        print("Mesa eliminada con éxito:", id_mesa)
        return '', 204
