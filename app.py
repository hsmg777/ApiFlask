import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS  # Importar Flask-CORS
from controllers.Usuario import blp as UserBluePrint
from db import init_db, db

def createApp():
    app = Flask(__name__)
    
    # Configuración general
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "IngWebAPI"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Configuración de la base de datos MySQL usando la variable de entorno `MYSQL_PUBLIC_URL`
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_PUBLIC_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa la base de datos con la aplicación
    init_db(app)
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    api = Api(app)
    
    # Registro de blueprints
    api.register_blueprint(UserBluePrint)
    
    return app

if __name__ == '__main__':
    app = createApp()
    app.run(debug=True)
