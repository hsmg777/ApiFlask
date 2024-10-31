from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Orden import Orden
from db import db
from schemas.OrdenSchema import OrdenSchema
from marshmallow import ValidationError

blp = Blueprint("Orden", __name__, url_prefix="/api/orden", description="CRUD Orden")

orden_schema = OrdenSchema()
ordenes_schema = OrdenSchema(many=True)

@blp.route('/')
class OrdenList(MethodView):
    @blp.response(200, OrdenSchema(many=True))
    def get(self):
        """Obtener todas las órdenes"""
        try:
            ordenes = Orden.query.all()
            return ordenes
        except Exception as e:
            print(f"Error al obtener órdenes: {e}")
            abort(500, message="Error al obtener órdenes")

    @blp.arguments(OrdenSchema)
    @blp.response(201, OrdenSchema)
    def post(self, data):
        """Crear una nueva orden"""
        try:
            nueva_orden = Orden(
                id_plato=data['id_plato'],
                id_mesa=data['id_mesa'],
                cantidad=data['cantidad'],
                observacion=data.get('observacion')
            )
            db.session.add(nueva_orden)
            db.session.commit()
            print("Orden creada con éxito:", nueva_orden.id_orden)
            return nueva_orden
        except Exception as e:
            print(f"Error al crear orden: {e}")
            abort(500, message="Error al crear orden")


@blp.route('/<int:id_orden>')
class OrdenResource(MethodView):
    @blp.response(200, OrdenSchema)
    def get(self, id_orden):
        """Obtener una orden por ID"""
        orden = Orden.query.get(id_orden)
        if orden is None:
            abort(404, message="Orden no encontrada")
        return orden

    @blp.arguments(OrdenSchema)
    @blp.response(200, OrdenSchema)
    def put(self, data, id_orden):
        """Actualizar una orden"""
        orden = Orden.query.get(id_orden)
        if orden is None:
            abort(404, message="Orden no encontrada")

        # Actualiza los campos
        orden.id_plato = data['id_plato']
        orden.id_mesa = data['id_mesa']
        orden.cantidad = data['cantidad']
        orden.observacion = data.get('observacion')
        
        db.session.commit()
        print("Orden actualizada con éxito:", orden.id_orden)
        return orden

    @blp.response(204)
    def delete(self, id_orden):
        """Eliminar una orden"""
        orden = Orden.query.get(id_orden)
        if orden is None:
            abort(404, message="Orden no encontrada")
        
        db.session.delete(orden)
        db.session.commit()
        print("Orden eliminada con éxito:", id_orden)
        return '', 204
