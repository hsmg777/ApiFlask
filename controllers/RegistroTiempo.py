from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.RegistroTiempo import RegistroTiempo
from models.Usuario import Usuario
from models.Orden import Orden
from models.Plato import Plato
from db import db
from schemas.RegistroTiempoSchema import RegistroTiempoSchema
from schemas.FechaRangoSchema import FechaRangoSchema
from schemas.PlatosChefSchema import PlatosChefSchema
from datetime import datetime, timedelta

blp = Blueprint("RegistroTiempo", __name__, url_prefix="/api/registrotiempo", description="CRUD Registro de Tiempo")

FechaRangoSchema = FechaRangoSchema()
PlatosChefSchema = PlatosChefSchema()
registro_tiempo_schema = RegistroTiempoSchema()
registros_tiempo_schema = RegistroTiempoSchema(many=True)

@blp.route('/top3/<int:id_plato>')
class RegistroTiempoTop3(MethodView):
    def get(self, id_plato):
        """Obtener el top 3 de registros con menor tiempo total para un plato específico"""
        try:
            # Query para obtener el top 3
            registros = db.session.query(
                RegistroTiempo.id_registroTiempo,
                RegistroTiempo.fecha,
                RegistroTiempo.tiempoInicio,
                RegistroTiempo.tiempoFin,
                RegistroTiempo.tiempoTotal,
                Usuario.Cedula.label("cedula"),
                (Usuario.Nombre + ' ' + Usuario.Apellido).label("nombres"),
                Plato.nombre.label("nombre_plato")
            ).join(Usuario, RegistroTiempo.id_User == Usuario.id_User)\
             .outerjoin(Plato, RegistroTiempo.id_plato == Plato.id_plato)\
             .filter(RegistroTiempo.tiempoTotal.isnot(None))\
             .filter(RegistroTiempo.id_plato == id_plato)\
             .order_by(RegistroTiempo.tiempoTotal.asc())\
             .limit(3)\
             .all()

            # Convertir los resultados a un formato JSON
            registros_dict = [
                {
                    "id_registroTiempo": registro.id_registroTiempo,
                    "fecha": registro.fecha.strftime('%Y-%m-%d'),
                    "tiempoInicio": registro.tiempoInicio.strftime('%H:%M:%S') if registro.tiempoInicio else None,
                    "tiempoFin": registro.tiempoFin.strftime('%H:%M:%S') if registro.tiempoFin else None,
                    "tiempoTotal": registro.tiempoTotal.strftime('%H:%M:%S') if registro.tiempoTotal else None,
                    "cedula": registro.cedula,
                    "nombres": registro.nombres,
                    "nombre_plato": registro.nombre_plato,
                }
                for registro in registros
            ]
            return jsonify(registros_dict)
        except Exception as e:
            print(f"Error al obtener el top 3 de registros de tiempo: {e}")
            abort(500, message="Error al obtener el top 3 de registros de tiempo")


@blp.route('/')
class RegistroTiempoList(MethodView):
    def get(self):
        """Obtener todos los registros de tiempo"""
        try:
            registros = db.session.query(
                RegistroTiempo.id_registroTiempo,
                RegistroTiempo.fecha,
                RegistroTiempo.tiempoInicio,
                RegistroTiempo.tiempoFin,
                RegistroTiempo.tiempoTotal,
                Usuario.Cedula.label("cedula"),
                (Usuario.Nombre + ' ' + Usuario.Apellido).label("nombres"),
                Plato.nombre.label("nombre_plato")
            ).join(Usuario, RegistroTiempo.id_User == Usuario.id_User)\
             .outerjoin(Plato, RegistroTiempo.id_plato == Plato.id_plato)\
             .all()

            registros_dict = [
                {
                    "id_registroTiempo": registro.id_registroTiempo,
                    "fecha": registro.fecha.strftime('%Y-%m-%d'),
                    "tiempoInicio": registro.tiempoInicio.strftime('%H:%M:%S') if registro.tiempoInicio else None,
                    "tiempoFin": registro.tiempoFin.strftime('%H:%M:%S') if registro.tiempoFin else None,
                    "tiempoTotal": registro.tiempoTotal.strftime('%H:%M:%S') if registro.tiempoTotal else None,
                    "cedula": registro.cedula,
                    "nombres": registro.nombres,
                    "nombre_plato": registro.nombre_plato,
                }
                for registro in registros
            ]
            return jsonify(registros_dict)
        except Exception as e:
            print(f"Error al obtener registros de tiempo: {e}")
            abort(500, message="Error al obtener registros de tiempo")

    @blp.arguments(RegistroTiempoSchema)
    @blp.response(201, RegistroTiempoSchema)
    def post(self, data):
        """Crear un nuevo registro de tiempo"""
        try:
            nuevo_registro = RegistroTiempo(
                id_User=data['id_User'],
                id_plato=data.get('id_plato'),
                fecha=data['fecha'],
                tiempoInicio=data['tiempoInicio'],
                tiempoFin=data.get('tiempoFin'),
                tiempoTotal=data.get('tiempoTotal')
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            print("Registro de tiempo creado con éxito:", nuevo_registro.id_registroTiempo)
            return nuevo_registro
        except Exception as e:
            print(f"Error al crear registro de tiempo: {e}")
            abort(500, message="Error al crear registro de tiempo")

@blp.route('/<int:id_registroTiempo>')
class RegistroTiempoResource(MethodView):
    @blp.response(200, RegistroTiempoSchema)
    def get(self, id_registroTiempo):
        """Obtener un registro de tiempo por ID"""
        registro = RegistroTiempo.query.get(id_registroTiempo)
        if registro is None:
            abort(404, message="Registro de tiempo no encontrado")
        return registro

    @blp.arguments(RegistroTiempoSchema)
    @blp.response(200, RegistroTiempoSchema)
    def put(self, data, id_registroTiempo):
        """Actualizar un registro de tiempo"""
        registro = RegistroTiempo.query.get(id_registroTiempo)
        if registro is None:
            abort(404, message="Registro de tiempo no encontrado")

        registro.id_User = data['id_User']
        registro.id_plato = data.get('id_plato')
        registro.fecha = data['fecha']
        registro.tiempoInicio = data['tiempoInicio']
        registro.tiempoFin = data.get('tiempoFin')

        # Calcular tiempo total si tiempoInicio y tiempoFin están presentes
        if registro.tiempoInicio and registro.tiempoFin:
            tiempo_inicio = datetime.combine(registro.fecha, registro.tiempoInicio)
            tiempo_fin = datetime.combine(registro.fecha, registro.tiempoFin)
            tiempo_total = tiempo_fin - tiempo_inicio
            registro.tiempoTotal = (datetime.min + tiempo_total).time()

        db.session.commit()
        print("Registro de tiempo actualizado con éxito:", registro.id_registroTiempo)
        return registro

    @blp.response(204)
    def delete(self, id_registroTiempo):
        """Eliminar un registro de tiempo"""
        registro = RegistroTiempo.query.get(id_registroTiempo)
        if registro is None:
            abort(404, message="Registro de tiempo no encontrado")

        db.session.delete(registro)
        db.session.commit()
        print("Registro de tiempo eliminado con éxito:", id_registroTiempo)
        return '', 204

#CHEF MAS TOP POR FECHAS
@blp.route('/chefmastop', methods=['POST'])
class ChefMasRapido(MethodView):
    @blp.arguments(FechaRangoSchema)
    def post(self, data):
        """Obtener el chef más rápido dentro de un rango de fechas"""
        try:
            fecha_inicio = data['fecha_inicio']
            fecha_fin = data['fecha_fin']

            # Query para obtener el chef más rápido
            resultado = db.session.query(
                RegistroTiempo.id_User.label('ChefID'),
                (Usuario.Nombre + ' ' + Usuario.Apellido).label('ChefNombre'),
                db.func.avg(db.func.datediff(db.text('SECOND'), RegistroTiempo.tiempoInicio, RegistroTiempo.tiempoFin)).label('TiempoPromedioSegundos')
            ).join(Usuario, RegistroTiempo.id_User == Usuario.id_User)\
             .join(Plato, RegistroTiempo.id_plato == Plato.id_plato)\
             .join(Orden, Plato.id_plato == Orden.id_plato)\
             .filter(Orden.fecha.between(fecha_inicio, fecha_fin))\
             .group_by(RegistroTiempo.id_User, Usuario.Nombre, Usuario.Apellido)\
             .order_by(db.text('TiempoPromedioSegundos ASC'))\
             .first()

            if not resultado:
                return jsonify({"message": "No se encontraron chefs en el rango de fechas especificado"}), 404

            chef_dict = {
                "ChefID": resultado.ChefID,
                "ChefNombre": resultado.ChefNombre,
                "TiempoPromedioSegundos": resultado.TiempoPromedioSegundos
            }
            return jsonify(chef_dict)

        except Exception as e:
            print(f"Error al obtener el chef más rápido: {e}")
            abort(500, message="Error al obtener el chef más rápido")

#3platos mas rapidos del chef
@blp.route('/platoschef', methods=['POST'])
class PlatosChef(MethodView):
    @blp.arguments(PlatosChefSchema)
    def post(self, data):
        """Obtener los platos con menor tiempo de un chef específico dentro de un rango de fechas"""
        try:
            id_chef = data['idChef']
            fecha_inicio = data['fecha_inicio']
            fecha_fin = data['fecha_fin']

            # Query para obtener los platos del chef
            resultado = db.session.query(
                RegistroTiempo.id_plato,
                Plato.nombre.label('PlatoNombre'),
                db.func.min(RegistroTiempo.tiempoTotal).label('TiempoMinimo')
            ).join(Plato, RegistroTiempo.id_plato == Plato.id_plato)\
             .filter(RegistroTiempo.id_User == id_chef)\
             .filter(RegistroTiempo.fecha.between(fecha_inicio, fecha_fin))\
             .group_by(RegistroTiempo.id_plato, Plato.nombre)\
             .order_by(db.text('TiempoMinimo ASC'))\
             .all()

            # Verificar si se encontraron resultados
            if not resultado:
                return jsonify({"message": "No se encontraron platos para el chef especificado en el rango de fechas"}), 404

            # Convertir los resultados a formato JSON
            platos_dict = [
                {
                    "id_plato": plato.id_plato,
                    "PlatoNombre": plato.PlatoNombre,
                    "TiempoMinimo": plato.TiempoMinimo
                }
                for plato in resultado
            ]

            return jsonify(platos_dict)

        except Exception as e:
            print(f"Error al obtener los platos del chef: {e}")
            abort(500, message="Error al obtener los platos del chef")
