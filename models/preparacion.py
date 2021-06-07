from operator import pos

from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types


class PreparacionModel(base_de_datos.Model):
    __tablename__ = "preparaciones"
    preparacionId = Column(name='id', primary_key=True, autoincrement=True,
                           unique=True, type_=types.Integer, nullable=False)
    preparacionOrden = Column(
        name='orden', type_=types.Integer, nullable=False)
    preparacionDescripcion = Column(
        name='descripcion', type_=types.Text, nullable=False)
    # ONDELETE sirve para indicar que accion tomaran todas las FK cuando una pk sea eliminada
    # CASCADE => Eliminará en forma de cascada primero la PK y luego todas sus FK
    # DELETE => Se eliminan y dejará a las FK con el mismo valor generando informacion incorrecta
    # RESTRICT => restringir la eliminacion siempre y cuando tenga FK existentes
    # None => no hagas nada
    postre = Column(ForeignKey(column='postres.id', ondelete='CASCADE'),
                    name='postre_id', type_=types.Integer, nullable=False)

    # En ORM las tablas se llaman modelos
    def __init__(self, orden, descripcion, postre_id):
        self.preparacionOrden = orden
        self.preparacionDescripcion = descripcion
        self.postre = postre_id

    def save(self):
        base_de_datos.session.add(self)    
        base_de_datos.session.commit()    

    def json(self): 
        return { 
            "id": self.preparacionId, 
            "orden": self.preparacionOrden, 
            "descripcion": self.preparacionDescripcion, 
            "postre": self.postre 
            }
