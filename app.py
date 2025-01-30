# app.py

import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from db import init_db
from controllers.Usuario import blp as UsuarioBlue
from controllers.Plato import blp as PlatoBlue
from controllers.Orden import blp as OrdenBlue
from controllers.Mesa import blp as MesaBlue
from controllers.RegistroTiempo import blp as TiempoBlue
import urllib.parse

from extensions import socketio

from controllers.observer_pattern import Subject, ChefObserver

def create_app():
    app = Flask(__name__)

    # Configuración General
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CORE_REST_API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configuración de la Base de Datos
    server = "Jorgeimlz\\SQLEXPRESS"
    database = "IngWeb"
    driver = "ODBC Driver 17 for SQL Server"

    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    )

    connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar la Base de Datos y CORS
    init_db(app)
    CORS(app)

    # Inicializar SocketIO con la aplicación Flask
    socketio.init_app(app, cors_allowed_origins="*")

    # Registrar Blueprints
    api = Api(app)
    api.register_blueprint(OrdenBlue)
    api.register_blueprint(TiempoBlue)
    api.register_blueprint(PlatoBlue)
    api.register_blueprint(UsuarioBlue)
    api.register_blueprint(MesaBlue)

    # ----------------------------
    # PATRÓN OBSERVER: Instancias
    # ----------------------------
    # Crear un sujeto global para notificar pedidos nuevos
    subject = Subject()

    # Crear un observador 'Chef'
    chef_observer = ChefObserver()

    # Suscribir al observador al sujeto
    subject.attach(chef_observer)

    # Guardar el sujeto en la configuración de la aplicación para uso futuro
    app.config['ORDER_SUBJECT'] = subject

    return app

app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación usando SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
