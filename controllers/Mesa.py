from flask import jsonify, request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Mesa import Mesa
from db import db
from schemas.MesaSchema import MesaSchema
from schemas.LoginMesaSchema import LoginMesaSchema
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

blp = Blueprint("Mesa", __name__, url_prefix="/api/mesa", description="CRUD Mesa")

mesa_schema = MesaSchema()
mesas_schema = MesaSchema(many=True)

# Manejador global para OPTIONS
@blp.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

# validar nombre y contraseña de mesa
@blp.route('/validate', methods=['POST'])
@blp.arguments(LoginMesaSchema)
def validar_mesa(datos):
    """
    Valida el nombre y la contraseña de una mesa y devuelve el id_mesa si es válida.
    """
    try:
        nombre = datos.get("nombre")
        passw = datos.get("passw")

        if not nombre or not passw:
            abort(400, message="Faltan parámetros de entrada")

        mesa = Mesa.query.filter_by(nombre=nombre, passw=passw).first()

        if mesa:
            logger.debug("Mesa encontrada: %s", mesa.nombre)
            return jsonify({"valid": True, "id_mesa": mesa.id_mesa}), 200
        else:
            logger.debug("Mesa no encontrada para nombre: %s", nombre)
            return jsonify({"valid": False}), 401  
    except Exception as e:
        logger.error("Error en validar_mesa: %s", e)
        abort(500, message="Error interno del servidor")


# CRUD Mesa
@blp.route('/', methods=['GET', 'POST', 'OPTIONS'])
class MesaList(MethodView):

    def get(self):
        """Obtener todas las mesas"""
        try:
            mesas = Mesa.query.all()
            logger.debug("Mesas obtenidas: %s", mesas)
            return jsonify(mesas_schema.dump(mesas)), 200
        except Exception as e:
            logger.error("Error al obtener mesas: %s", e)
            abort(500, message="Error al obtener mesas")

    @blp.arguments(MesaSchema)
    @blp.response(201, MesaSchema)
    def post(self, data):
        """Crear una nueva mesa"""
        try:
            nueva_mesa = Mesa(nombre=data['nombre'], passw=data['passw'])
            db.session.add(nueva_mesa)
            db.session.commit()
            logger.debug("Mesa creada con éxito: %s", nueva_mesa.nombre)
            return jsonify(mesa_schema.dump(nueva_mesa)), 201
        except Exception as e:
            logger.error("Error al crear mesa: %s", e)
            abort(500, message="Error al crear mesa")


@blp.route('/<int:id_mesa>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
class MesaResource(MethodView):

    def get(self, id_mesa):
        """Obtener una mesa por ID"""
        try:
            mesa = Mesa.query.get(id_mesa)
            if mesa is None:
                logger.error("Mesa no encontrada: %d", id_mesa)
                abort(404, message="Mesa no encontrada")
            logger.debug("Mesa obtenida: %s", mesa.nombre)
            return jsonify(mesa_schema.dump(mesa)), 200
        except Exception as e:
            logger.error("Error al obtener mesa: %s", e)
            abort(500, message="Error al obtener mesa")

    @blp.arguments(MesaSchema)
    @blp.response(200, MesaSchema)
    def put(self, data, id_mesa):
        """Actualizar una mesa"""
        try:
            mesa = Mesa.query.get(id_mesa)
            if mesa is None:
                logger.error("Mesa no encontrada para actualizar: %d", id_mesa)
                abort(404, message="Mesa no encontrada")

            mesa.nombre = data['nombre']
            mesa.passw = data['passw']
            db.session.commit()
            logger.debug("Mesa actualizada con éxito: %s", mesa.nombre)
            return jsonify(mesa_schema.dump(mesa)), 200
        except Exception as e:
            logger.error("Error al actualizar mesa: %s", e)
            abort(500, message="Error al actualizar mesa")

    @blp.response(204)
    def delete(self, id_mesa):
        """Eliminar una mesa"""
        try:
            mesa = Mesa.query.get(id_mesa)
            if mesa is None:
                logger.error("Mesa no encontrada para eliminar: %d", id_mesa)
                abort(404, message="Mesa no encontrada")

            db.session.delete(mesa)
            db.session.commit()
            logger.debug("Mesa eliminada con éxito: %d", id_mesa)
            return '', 204
        except Exception as e:
            logger.error("Error al eliminar mesa: %s", e)
            abort(500, message="Error al eliminar mesa")
