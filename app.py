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

def create_app():  # Renombré la función para usar snake_case (convención de Python)
    app = Flask(__name__)

    # Configuración general
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CORE_REST_API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Configuración de la base de datos
    server = 'tcp:ingwebserver.database.windows.net,1433'
    database = 'IngWeb'
    username = 'aurora'
    password = 'Mamifer_1'  # Reemplaza con la contraseña real
    driver = 'ODBC Driver 17 for SQL Server'

    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos
    init_db(app)

    # Configuración de CORS
    CORS(app)

    # Registro de blueprints
    api = Api(app)
    api.register_blueprint(OrdenBlue)
    api.register_blueprint(TiempoBlue)
    api.register_blueprint(PlatoBlue)
    api.register_blueprint(UsuarioBlue)
    api.register_blueprint(MesaBlue)

    return app

# Asegúrate de que la variable `app` sea global y esté definida correctamente
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
