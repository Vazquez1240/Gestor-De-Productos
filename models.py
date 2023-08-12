import db
from sqlalchemy import Column, Integer, Float, String

class Producto(db.Base):
    __tablename__ = "productos"
    __table_args__ = {'sqlite_autoincrement': True}
    id_producto = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    num_producto = Column(Integer, nullable=False)
    categoria = Column(String)

    def __init__(self, nombre, precio, num_producto, categoria):
        self.nombre = nombre
        self.precio = precio
        self.num_producto = num_producto
        self.categoria = categoria

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.id_producto, self.nombre, self.precio,self.num_producto, self.categoria)