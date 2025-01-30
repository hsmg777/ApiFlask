# controllers/Orden.py

from flask import request, jsonify, current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Orden import Orden
from models.Plato import Plato
from models.Mesa import Mesa
from db import db
from schemas.OrdenSchema import OrdenSchema

blp = Blueprint("Orden", __name__, url_prefix="/api/orden", description="CRUD Orden")

orden_schema = OrdenSchema()
ordenes_schema = OrdenSchema(many=True)

@blp.route('/')
class OrdenList(MethodView):

    def get(self):
        """Obtener todas las órdenes"""
        try:
            resultados = Orden.query.all()
            ordenes = [
                {
                    "id_orden": o.id_orden,
                    "id_plato": o.id_plato,
                    "id_mesa": o.id_mesa,
                    "cantidad": o.cantidad,
                    "observacion": o.observacion,
                    "estado": o.estado,
                    "fecha": o.fecha.strftime('%Y-%m-%d') if o.fecha else None
                }
                for o in resultados
            ]
            return jsonify(ordenes), 200
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
                observacion=data.get('observacion'),
                estado=data.get('estado', 'Pendiente')
            )
            db.session.add(nueva_orden)
            db.session.commit()

            print("Orden creada con éxito:", nueva_orden.id_orden)

            # --------------------------------
            # 1) Recuperar el subject del app
            # --------------------------------
            subject = current_app.config.get("ORDER_SUBJECT")
            if subject:
                # ----------------------------------------
                # 2) Notificar a todos los observadores
                # ----------------------------------------
                # Obtener información adicional como el nombre del plato
                plato = Plato.query.get(nueva_orden.id_plato)
                mesa = Mesa.query.get(nueva_orden.id_mesa)
                order_info = {
                    "id_orden": nueva_orden.id_orden,
                    "id_plato": nueva_orden.id_plato,
                    "Plato": plato.nombre if plato else "Desconocido",
                    "id_mesa": nueva_orden.id_mesa,
                    "Mesa": mesa.nombre if mesa else "Desconocida",
                    "cantidad": nueva_orden.cantidad,
                    "estado": nueva_orden.estado
                }
                subject.notify(order_info)

            return nueva_orden
        except Exception as e:
            print(f"Error al crear orden: {e}")
            abort(500, message="Error al crear orden")
            
@blp.route('/detalles')
class OrdenDetalles(MethodView):
    def get(self):
        """Obtener detalles de órdenes con Mesa y Plato"""
        try:
            resultados = db.session.query(
                Orden.id_orden,
                Mesa.nombre.label("Mesa"),
                Mesa.id_mesa,
                Plato.nombre.label("Plato"),
                Orden.cantidad,
                Orden.observacion,
                Orden.estado,
                Orden.fecha
            ).join(Plato, Orden.id_plato == Plato.id_plato).join(Mesa, Orden.id_mesa == Mesa.id_mesa).all()

            detalles_ordenes = [
                {
                    "id_orden": r.id_orden,
                    "id_mesa" : r.id_mesa,
                    "Mesa": r.Mesa,
                    "Plato": r.Plato,
                    "Cantidad": r.cantidad,
                    "Observacion": r.observacion,
                    "Estado": r.estado,
                    "Fecha": r.fecha
                }
                for r in resultados
            ]
            return jsonify(detalles_ordenes), 200
        except Exception as e:
            print(f"Error al obtener detalles de órdenes: {e}")
            abort(500, message="Error al obtener detalles de órdenes")

@blp.route('/<int:id_orden>')
class OrdenResource(MethodView):

    @blp.response(200, OrdenSchema)
    def get(self, id_orden):
        """Obtener una orden por ID"""
        try:
            orden = Orden.query.get(id_orden)
            if orden is None:
                abort(404, message="Orden no encontrada")
            return orden
        except Exception as e:
            print(f"Error al obtener orden: {e}")
            abort(500, message="Error al obtener orden")

    @blp.arguments(OrdenSchema)
    @blp.response(200, OrdenSchema)
    def put(self, data, id_orden):
        """Actualizar una orden"""
        try:
            orden = Orden.query.get(id_orden)
            if orden is None:
                abort(404, message="Orden no encontrada")

            orden.id_plato = data['id_plato']
            orden.id_mesa = data['id_mesa']
            orden.cantidad = data['cantidad']
            orden.observacion = data.get('observacion')
            orden.estado = data.get('estado', orden.estado)
            
            db.session.commit()
            print("Orden actualizada con éxito:", orden.id_orden)
            return orden
        except Exception as e:
            print(f"Error al actualizar orden: {e}")
            abort(500, message="Error al actualizar orden")

    @blp.response(204)
    def delete(self, id_orden):
        """Eliminar una orden"""
        try:
            orden = Orden.query.get(id_orden)
            if not orden:
                abort(404, message="Orden no encontrada")

            db.session.delete(orden)
            db.session.commit()
            print("Orden eliminada con éxito:", id_orden)
            return '', 204
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar orden: {e}")
            abort(500, message="Error interno al eliminar orden")
