from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Plato import Plato
from models.Usuario import Usuario
from db import db
from schemas.PlatoSchema import PlatoSchema
from sqlalchemy import func

blp = Blueprint("Plato", __name__, url_prefix="/api/plato", description="CRUD Plato")

plato_schema = PlatoSchema()
platos_schema = PlatoSchema(many=True)

# Manejador global para solicitudes OPTIONS
@blp.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

@blp.route('/', methods=["GET", "POST", "OPTIONS"])
class PlatoList(MethodView):
    @blp.response(200, PlatoSchema(many=True))
    def get(self):
        """Obtener todos los platos con información del creador"""
        try:
            # Consulta personalizada con join
            platos = db.session.query(
                Plato.id_plato,
                Plato.id_User,
                func.concat(Usuario.Nombre, ' ', Usuario.Apellido).label('creador'),
                Plato.nombre.label('nombre'),
                Plato.precio.label('precio'),
                Plato.descripcion.label('descripcion'),
                Plato.urlImg.label('imagen')
            ).join(Usuario, Plato.id_User == Usuario.id_User).all()

            # Formateo de resultados en un diccionario para devolver como JSON
            platos_dict = [
                {
                    "id_plato": plato.id_plato,
                    "id_User": plato.id_User,
                    "creador": plato.creador,
                    "nombre": plato.nombre,
                    "precio": plato.precio,
                    "descripcion": plato.descripcion,
                    "imagen": plato.imagen
                }
                for plato in platos
            ]
            return jsonify(platos_dict)
        except Exception as e:
            print(f"Error al obtener platos: {e}")
            abort(500, message="Error al obtener platos")

    def post(self):
        """Crear un nuevo plato"""
        data = request.get_json()  # Recibe los datos de la solicitud directamente
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
            return plato_schema.dump(nuevo_plato), 201
        except Exception as e:
            print(f"Error al crear plato: {e}")
            abort(500, message="Error al crear plato")


@blp.route('/<int:id_plato>', methods=["GET", "PUT", "DELETE", "OPTIONS"])
class PlatoResource(MethodView):
    @blp.response(200, PlatoSchema)
    def get(self, id_plato):
        """Obtener un plato por ID"""
        plato = Plato.query.get(id_plato)
        if plato is None:
            abort(404, message="Plato no encontrado")
        return plato

    def put(self, id_plato):
        """Actualizar un plato"""
        data = request.get_json()  # Recibe los datos de la solicitud directamente
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
        return plato_schema.dump(plato), 200

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
