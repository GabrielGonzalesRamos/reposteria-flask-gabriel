from controllers.preparacion import PreparacionesController
from flask import Flask, request
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from flask_restful import Api
from controllers.postre import BusquedaPostre, PostresController, PostreController
from models.postre import PostreModel
from models.preparacion import PreparacionModel
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
from controllers.ingrediente import IngredienteController, IngredientesController
from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()

# Configuramos el SWAGGET EN EL FLASK

SWAGGER_URL = "" #Indica en  que ruta se encuentra la doc
API_URL = "/static/swagger.json" #Indica la ubicacion del archivo json
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Reposteria Flask - Swagger Documentation"
    }
)
# FIN DE LA CONFIGURACION

app = Flask(__name__)
# Sirve para registrar en el caso que nosotros tengamos un proyecto interno para agregarlo a un proyecto principal

app.register_blueprint(swaggerui_blueprint)
api = Api(app)
# dialec
print(environ.get("DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
# Si se establece en True, FLask-SQLAlchemy rastrearan las modificaciones
# de los objetos y lanzará señales.
# Su valor predeterminado es None, igual habilita el tracking pero emite
# una advertencia  que se deshabilitará de manera predeterminada en futuras versiones.
# Esto consume memoria adicional y si no se va a utliizar es mejor desactiviarlo = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# iniciar la bd para darle las credenciales definidas en el config
base_de_datos.init_app(app)

# crea todas las tablas definidas en los modelos en el proyecto
base_de_datos.create_all(app=app)
# Sirve para eliminar todas las tablas y limpiar todas las bases de datos
# Esto se utilizar en fases tempranas del proyecto y antes de pasar a produccion si 
# usamos la misma bd, para limpiar la informacion falsa
#base_de_datos.drop_all(app=app)

@app.route("/")
def initial_controller():
    return {
        "message": "Welcome  API 🧁"
    }


# DEFINO LAS RUTAS USANDO EL FLASK RESTFUL
api.add_resource(PostresController, "/postres")
api.add_resource(PostreController, "/postres/<int:id>")
api.add_resource(BusquedaPostre, "/busqueda_postre")
api.add_resource(PreparacionesController, "/preparaciones", "/preparaciones/<int:postre_id>")
api.add_resource(IngredientesController, "/ingredientes")
api.add_resource(IngredienteController, "/ingredientes/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
