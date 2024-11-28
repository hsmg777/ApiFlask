from flask import Flask
from flask_smorest import Api
from flask_cors import CORS  # Importar Flask-CORS
from controllers.Usuario import blp as UsuarioBlue
from controllers.Plato import blp as PlatoBlue
from controllers.Orden import blp as OrdenBlue
from controllers.Mesa import blp as MesaBlue
from controllers.RegistroTiempo import blp as TiempoBlue
from db import init_db, db
import urllib.parse

def createApp():
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
    
    # Inicializa la base de datos con la aplicación
    init_db(app)
    
    # Configurar CORS
    CORS(app)
    
    api = Api(app)
    
    # Registro de blueprints
    api.register_blueprint(OrdenBlue)
    api.register_blueprint(TiempoBlue)
    api.register_blueprint(PlatoBlue)
    api.register_blueprint(UsuarioBlue)
    api.register_blueprint(MesaBlue)
    
    return app

if __name__ == '__main__':
    app = createApp()
    app.run(debug=True)
