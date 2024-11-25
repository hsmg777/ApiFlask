from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.Usuario import Usuario
from db import db
from schemas.UsuarioSchema import UsuarioSchema
from schemas.LoginSchema import LoginSchema
from marshmallow import ValidationError

blp = Blueprint("Usuario", __name__, url_prefix="/api/usuario", description="CRUD Usuario")

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# Validación de Username y Contrasenia
@blp.route('/validate', methods=['POST'])
@blp.arguments(LoginSchema)
def validar_usuario(datos):
    try:
        username = datos.get("username")
        contrasenia = datos.get("contrasenia")

        if not username or not contrasenia:
            abort(400, message="Faltan parámetros de entrada")

        usuario = Usuario.query.filter_by(Username=username, Contrasenia=contrasenia).first()

        if usuario:
            print("Usuario encontrado:", usuario.Username)
            return jsonify({"valid": True, "isAdmin": usuario.isAdmin, "id_User": usuario.id_User}), 200
        else:
            print("Usuario no encontrado")
            return jsonify({"valid": False}), 401
    except Exception as e:
        print(f"Error en validar_usuario: {e}")
        abort(500, message="Error interno del servidor")

# CRUD Usuario
@blp.route('/')
class UsuariosList(MethodView):
    @blp.response(200, UsuarioSchema(many=True))
    def get(self):
        try:
            usuarios = Usuario.query.all()
            print("Usuarios encontrados:", usuarios)
            # Asegurarse de que la respuesta esté en formato JSON
            return jsonify(usuarios_schema.dump(usuarios))
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            abort(500, message="Error al obtener usuarios")

    @blp.arguments(UsuarioSchema)
    @blp.response(201, UsuarioSchema)
    def post(self, data):
        try:
            print("Datos recibidos para crear usuario:", data)
            # Incluye el campo isAdmin al crear el usuario
            nuevo_usuario = Usuario(
                Username=data['Username'],
                Contrasenia=data['Contrasenia'],
                Nombre=data['Nombre'],
                Apellido=data['Apellido'],
                Cedula=data['Cedula'],
                Telefono=data['Telefono'],
                isAdmin=data.get('isAdmin', 'N')  # Valor predeterminado 'N' si no se proporciona
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            print("Usuario creado con éxito:", nuevo_usuario.Username)
            return jsonify(usuario_schema.dump(nuevo_usuario)), 201
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            abort(500, message="Error al crear usuario")

@blp.route('/<int:id_User>')
class UsuarioResource(MethodView):
    @blp.response(200, UsuarioSchema)
    def get(self, id_User):
        try:
            usuario = Usuario.query.get(id_User)
            if usuario is None:
                print("Usuario no encontrado:", id_User)
                abort(404, message="Usuario no encontrado")
            print("Usuario encontrado:", usuario.Username)
            return jsonify(usuario_schema.dump(usuario))
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            abort(500, message="Error al obtener usuario")

    @blp.arguments(UsuarioSchema)
    @blp.response(200, UsuarioSchema)
    def put(self, data, id_User):
        try:
            usuario = Usuario.query.get(id_User)
            if usuario is None:
                print("Usuario no encontrado para actualizar:", id_User)
                abort(404, message="Usuario no encontrado")

            # Actualizar campos
            usuario.Username = data['Username']
            usuario.Contrasenia = data['Contrasenia']
            usuario.Nombre = data['Nombre']
            usuario.Apellido = data['Apellido']
            usuario.Cedula = data['Cedula']
            usuario.Telefono = data['Telefono']
            usuario.isAdmin = data.get('isAdmin', usuario.isAdmin)

            db.session.commit()
            print("Usuario actualizado con éxito:", usuario.Username)
            return jsonify(usuario_schema.dump(usuario))
        except KeyError as e:
            abort(400, message=f"Falta el campo {e.args[0]} en la solicitud.")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            abort(500, message="Error al actualizar usuario")

    @blp.response(204)
    def delete(self, id_User):
        try:
            usuario = Usuario.query.get(id_User)
            if usuario is None:
                print("Usuario no encontrado para eliminar:", id_User)
                abort(404, message="Usuario no encontrado")
            db.session.delete(usuario)
            db.session.commit()
            print("Usuario eliminado con éxito:", id_User)
            return '', 204
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            abort(500, message="Error al eliminar usuario")
