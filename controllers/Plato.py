from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Plato import Plato
from db import db
from schemas.PlatoSchema import PlatoSchema
from marshmallow import ValidationError

blp = Blueprint("Plato", __name__, url_prefix="/api/plato", description="CRUD Plato")

plato_schema = PlatoSchema()
platos_schema = PlatoSchema(many=True)

@blp.route('/')
class PlatoList(MethodView):
    @blp.response(200, PlatoSchema(many=True))
    def get(self):
        """Obtener todos los platos"""
        try:
            platos = Plato.query.all()
            return platos
        except Exception as e:
            print(f"Error al obtener platos: {e}")
            abort(500, message="Error al obtener platos")

    @blp.arguments(PlatoSchema)
    @blp.response(201, PlatoSchema)
    def post(self, data):
        """Crear un nuevo plato"""
        try:
            nuevo_plato = Plato(
                id_User=data['id_User'],
                nombre=data['nombre'],
                precio=data['precio'],
                descripcion=data.get('descripcion'),
                urlImg=data.get('urlImg')
            )
            db.session.add(nuevo_plato)
            db.session.commit()
            print("Plato creado con éxito:", nuevo_plato.nombre)
            return nuevo_plato
        except Exception as e:
            print(f"Error al crear plato: {e}")
            abort(500, message="Error al crear plato")


@blp.route('/<int:id_plato>')
class PlatoResource(MethodView):
    @blp.response(200, PlatoSchema)
    def get(self, id_plato):
        """Obtener un plato por ID"""
        plato = Plato.query.get(id_plato)
        if plato is None:
            abort(404, message="Plato no encontrado")
        return plato

    @blp.arguments(PlatoSchema)
    @blp.response(200, PlatoSchema)
    def put(self, data, id_plato):
        """Actualizar un plato"""
        plato = Plato.query.get(id_plato)
        if plato is None:
            abort(404, message="Plato no encontrado")

        # Actualiza los campos
        plato.id_User = data['id_User']
        plato.nombre = data['nombre']
        plato.precio = data['precio']
        plato.descripcion = data.get('descripcion')
        plato.urlImg = data.get('urlImg')

        db.session.commit()
        print("Plato actualizado con éxito:", plato.nombre)
        return plato

    @blp.response(204)
    def delete(self, id_plato):
        """Eliminar un plato"""
        plato = Plato.query.get(id_plato)
        if plato is None:
            abort(404, message="Plato no encontrado")
        
        db.session.delete(plato)
        db.session.commit()
        print("Plato eliminado con éxito:", id_plato)
        return '', 204
