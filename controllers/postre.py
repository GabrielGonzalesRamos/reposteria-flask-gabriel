# Un controlador es el comportamiento que va a tener mi API
# cuando se llame a determinada ruta
# /postres GET  => mostrar los postres
from operator import pos
from os import name

from sqlalchemy.orm import base
from models.postre import PostreModel
from flask_restful import Resource, reqparse
from config.conexion_bd import base_de_datos

# Serializador o serializer
# un pequeño filtro de lo que necesitará el post

# Agrupa los errores bundle_errors
serializerPostres = reqparse.RequestParser(bundle_errors=True)
serializerPostres.add_argument(
    'nombre', # nombre del atributo en el body
    type=str, # tipo de dato que me tiene que mandar
    required=True, # si es de caracter obligatorio o no 
    help="Falta el nombre", # mensaje de ayuda en el caso fuese obligatorio y no me lo mandase
    location='json' # en que parte del request me mandará, ya sea json (body) o url
)
serializerPostres.add_argument(
    'porcion',
    type=str,
    required=True,
    help="Falta la porcion CODE: {error_msg}",
    choices=('Familiar', 'Personal', 'Mediano'),
    location='json'
)



class PostresController(Resource):
    """Será la encargada de la gestion de todos los postres y su creacion"""
    def get(self):
        # SELECT * FROM postres;
        postres = PostreModel.query.all()
        resultado = []
        for postre in postres:
            resultado.append(postre.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }, 201

    def post(self):
        data = serializerPostres.parse_args()
        nuevoPostre = PostreModel(nombre=data.get('nombre'), porcion=data.get('porcion'))
        print(nuevoPostre)
        nuevoPostre.save()
        return {
            'success': True,
            'content': nuevoPostre.json(),
            'message': "Postre creado exitosamente"
        }, 201




class PostreController(Resource):
    def get(self, id):
        
        #La documentacion nativa de SQLAlchemy
        #otro_postre = base_de_datos.session.query(PostreModel).filter(PostreModel.postreId == id).first()
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId = id).first()
        #La documentacion del flask sql alchemy
        #postre = PostreModel.query.filter_by(postreId = id).first()
        
        print(postre)
        #print(otro_postre)
        #print(otro_postre_2)
        # verdadero if condicion else false
        return ({
            'success': True,
            #'content': postre.json() if postre else 'no hay postre',
            'content': postre.json(),
            'message': None
        }, 200)  if postre else ({
            'success': False,
            'content': None,
            'message': 'Postre no encontrado'
        }, 404)
    
    def put(self, id):
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        if postre:
            data = serializerPostres.parse_args()
            postre.postreNombre = data.get('nombre')
            postre.postrePorcion = data.get('porcion')
            postre.save()

            return {
                'succes': True,
                'content': postre.json(),
                'message': 'Postre actualizado correctamente'
            }, 201
        else:
            return {
                'succes': False,
                'content': None,
                'message': 'Postre no encontrado'
            }, 404    

    def delete(self, id):
        #  Método 1 
        # postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).delete()
        # base_de_datos.session.commit()
        # return {
        #     'success': True,
        #     'content': None,
        #     'message': 'Postre eliminado exitosamente'
        # }
        # Método 2
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        postre.delete()
        return {
            'success': True,
            'content': postre.json(),
            'message': 'Postre eliminado exitosamente'
        }

# Resource hace que el def get():, def post():, def delete():
class BusquedaPostre(Resource):
    serializerBusqueda = reqparse.RequestParser()
    serializerBusqueda.add_argument(
        'nombre',
        type=str,
        location='args',
        required=False
    )
    serializerBusqueda.add_argument(
        'porcion',
        type=str,
        location='args',
        choices=('Familiar', 'Personal', 'Mediano'),
        help='Opcion inválida escoger [Familiar, Personal, Mediano]',
        required=False
    )
    def get(self):
        filtros = self.serializerBusqueda.parse_args()
        if filtros.get('nombre') and filtros.get('porcion'):
            resultado = base_de_datos.session.query(PostreModel).filter_by(postreNombre=filtros.get('nombre'), postrePorcion=filtros.get('porcion')).all()
        elif filtros.get('nombre'):
            resultado = base_de_datos.session.query(PostreModel).filter_by(postreNombre=filtros.get('nombre')).all()
        elif filtros.get('porcion'):
            resultado = base_de_datos.session.query(PostreModel).filter_by(postrePorcion=filtros.get('porcion')).all()  
        else:
            return {
                'message': 'Necesitas dar al menos un parametro'
            }, 400
        postres = []
        for postre in resultado:
            postres.append(postre.json())
        return {
            'success': True,
            'content': postres,
            'message': "Exitoso"
        }    