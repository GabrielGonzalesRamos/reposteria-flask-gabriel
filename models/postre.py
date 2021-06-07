from sqlalchemy.orm import base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Integer
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm


class PostreModel(base_de_datos.Model):  # Esta clase será una tabla
    # Si no creo este atributo privado, el nombre de la tabla sería igual
    # al nombre de la clase "PostreModel"
    __tablename__ = "postres"

    postreId = Column(name='id', primary_key=True,
                      autoincrement=True, unique=True, type_=types.Integer)
    # Tipos de datos en Mayusculas posiblemente no puedan ser soportadas por algunas bases de datos
    postreNombre = Column(name='nombre', type_=types.String(length=45))
    postrePorcion = Column(name='porcion', type_=types.String(length=25))

    # El relationship sirve para indicar todos los "hijos" que puede
    # tener ese modelo (todas sus FK)
    # que pueden existir en determinado modelo
    # el backref creará un atributo virtual en el model del hijo
    # (Preparacion) para que pueda acceder a todo el objeto de PostreModel sin la necesidad
    # de hacer una sub consulta (creará un join cuando sea necesario)
    # lazy => defino cuando SQLAlchemy va a cargar la data adyacente de la base de datos
    # 'True' / 'select' => cargará todos los datos adyacentes
    # 'False' / 'joined' => solamente cargará cuando sea necesario (cuando se utilicen dichos datos)
    #  'subquery' =>  trabajará los datos PERO en una sub consulta
    # 'dynamic' => en este se pueden agregar filtros adicionales. SQLAlchemy devolverá otro objeto dentro de la clase
    preparaciones = orm.relationship(
        'PreparacionModel', backref='preparacionPostre', lazy=True)
    recetas = orm.relationship('RecetaModel', backref='recetaPostre')
    # Constructor

    def __init__(self, nombre, porcion):
        self.postreNombre = nombre
        self.postrePorcion = porcion

    def __str__(self):
        return "El posrte es {}".format(self.postreNombre)     

    def save(self):
        # El metodo session.add crea un nueva sesion en la bd y ademas
        # evita que se creen nuevas sesiones y asi relentizar la conexion a la bd
        # el metodo add sirve para agregar toda la instancia actual (mi nuevo postre) y corroborar con 
        # las columnas de la bd si todo esta correcto
        # esto ademas crea una transaccion en la cual sirve para agrupar varias sentencias de insert,
        # update, delete
        base_de_datos.session.add(self)
        # ahorta si todos los pasos de escritura, actualizacion y eliminacion de la db fueron exitosos
        # entonces se guardarán todos los cambios de manera permanente
        # todas las sesiones dentro de la misma instancia o entorno que esten pendiente de guardar
        # PERMANENTE sus cambios en la bd al usar el commit se guardar de forma permanente
        base_de_datos.session.commit()
        # metodo que sirve para cerrar la session de la bd
        #base_de_datos.session.close()

    def json(self):
        return {
            "id": self.postreId,
            "nombre": self.postreNombre,
            "postrePorcion": self.postrePorcion
        }
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()    