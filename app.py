from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from controllers.Usuario import blp as UserBluePrint
from controllers.Plato import blp as PlatoBlueprint
from controllers.Mesa import blp as MesaBlueprint
from controllers.Orden import blp as OrdenBlueprint
from controllers.RegistroHoras import blp as RegistroHorasBlueprint



from db import init_db, db
import urllib.parse

def createApp():
    app = Flask(__name__)
    
    # Configuración API
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "IngWebAPI"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Configuración bd
    server = '(localdb)\\MSSQLLocalDB'
    database = 'IngWeb'
    username = 'aurora'
    password = 'mamifer1'
    driver = 'ODBC Driver 17 for SQL Server'
    
    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
  
    init_db(app)
    
    # CORS

    CORS(app, resources={r"/api/*": {"origins": "https://preact-mauve.vercel.app"}})



    # blueprints
    api = Api(app)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(PlatoBlueprint)
    api.register_blueprint(MesaBlueprint)
    api.register_blueprint(OrdenBlueprint)
    api.register_blueprint(RegistroHorasBlueprint)



    
    return app

if __name__ == '__main__':
    app = createApp()
    app.run(debug=True)
