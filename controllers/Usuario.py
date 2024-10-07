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
    username = datos.get("username")
    contrasenia = datos.get("contrasenia")

    if not username or not contrasenia:
        abort(400, message="Faltan parámetros de entrada")

    usuario = Usuario.query.filter_by(Username=username, Contrasenia=contrasenia).first()

    if usuario:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False}), 401
# CRUD Usuario
@blp.route('/')
class UsuariosList(MethodView):
    @blp.response(200, UsuarioSchema(many=True))
    def get(self):
        usuarios = Usuario.query.all()
        return usuarios

    @blp.arguments(UsuarioSchema)
    @blp.response(201, UsuarioSchema)
    def post(self, data):
        nuevo_usuario = Usuario(
            Username=data['Username'],
            Contrasenia=data['Contrasenia'],
            Nombre=data['Nombre'],
            Apellido=data['Apellido'],
            Cedula=data['Cedula'],
            Telefono=data['Telefono']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

@blp.route('/<int:id_User>')
class UsuarioResource(MethodView):
    @blp.response(200, UsuarioSchema)
    def get(self, id_User):
        usuario = Usuario.query.get(id_User)
        if usuario is None:
            abort(404, message="Usuario no encontrado")
        return usuario

    @blp.arguments(UsuarioSchema)
    @blp.response(200, UsuarioSchema)
    def put(self, data, id_User):
        usuario = Usuario.query.get(id_User)
        if usuario is None:
            abort(404, message="Usuario no encontrado")

        # Verificar que los datos estén presentes correctamente en el cuerpo de la solicitud
        try:
            usuario.Username = data['Username']
            usuario.Contrasenia = data['Contrasenia']
            usuario.Nombre = data['Nombre']
            usuario.Apellido = data['Apellido']
            usuario.Cedula = data['Cedula']
            usuario.Telefono = data['Telefono']
        except KeyError as e:
            abort(400, message=f"Falta el campo {e.args[0]} en la solicitud.")

        # Guardar los cambios en la base de datos
        db.session.commit()
        return usuario

    @blp.response(204)
    def delete(self, id_User):
        usuario = Usuario.query.get(id_User)
        if usuario is None:
            abort(404, message="Usuario no encontrado")
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

