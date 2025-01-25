from src.database import pool
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey

Base = declarative_base()

class TB_USUARIOS(Base):
    __tablename__ = 'tb_usuarios'
    id_usuario = Column(Integer, primary_key=True)
    Nombre = Column(VARCHAR, nullable=False)
    Contraseña = Column(VARCHAR, nullable=False)
    Direccion = Column(VARCHAR, nullable=False)
    Correo = Column(VARCHAR, nullable=False, unique=True)
    Deleted = Column(Boolean, nullable=False, default=False)
    proyectos = relationship("TB_PROYECTOS", back_populates="usuario")

    def __repr__(self):
        return f"<TB_USUARIOS(id_usuario={self.id_usuario}, Nombre={self.Nombre}, Contraseña={self.Contraseña}, Direccion={self.Direccion}, Correo={self.Correo}, Deleted={self.Deleted})>"

class TB_FIGURAS(Base):
    __tablename__ = 'tb_figuras'
    id_figura = Column(Integer, primary_key=True)
    Area = Column(Integer, nullable=True, default=None)
    Perimetro = Column(Integer, nullable=True, default=None)
    Contenedor = Column(VARCHAR, nullable=True, default='')
    SHA256 = Column(VARCHAR, nullable=False)
    Deleted = Column(Boolean, nullable=False, default=False)
    proyectos = relationship("TB_PROYECTOS", back_populates="figura")

    def __repr__(self):
        return f"<TB_FIGURAS(id_figura={self.id_figura}, Area={self.Area}, Perimetro={self.Perimetro}, Contenedor={self.Contenedor}, SHA256={self.SHA256}, Deleted={self.Deleted})>"

class TB_MATERIAL_ESPESOR(Base):
    __tablename__ = 'tb_material_espesor'
    id_material_espesor = Column(Integer, primary_key=True)
    id_espesor = Column(Integer, ForeignKey("tb_espesores.id_espesor"), nullable=False)
    id_material = Column(Integer, ForeignKey("tb_materiales.id_material"), nullable=False)
    Espesor = relationship("TB_ESPESORES", back_populates="material_espesor")
    Material = relationship("TB_MATERIALES", back_populates="material_espesor")
    Deleted = Column(Boolean, nullable=False, default=False)
    proyectos = relationship("TB_PROYECTOS", back_populates="material_espesor")

    def __repr__(self):
        return f"<TB_MATERIAL_ESPESOR(id_material_espesor={self.id_material_espesor}, id_espesor={self.id_espesor}, id_material={self.id_material}, Deleted={self.Deleted})>"

class TB_ESPESORES(Base):
    __tablename__ = 'tb_espesores'
    id_espesor = Column(Integer, primary_key=True)
    Espesor = Column(Integer, nullable=False)
    Deleted = Column(Boolean, nullable=False, default=False)
    material_espesor = relationship("TB_MATERIAL_ESPESOR", back_populates="Espesor")

    def __repr__(self):
        return f"<TB_ESPESOR(id_espesor={self.id_espesor}, Espesor={self.Espesor}, Deleted={self.Deleted})>"

class TB_MATERIALES(Base):
    __tablename__ = 'tb_materiales'
    id_material = Column(Integer, primary_key=True)
    Nombre = Column(VARCHAR, nullable=False)
    Valor = Column(Integer, nullable=False)
    Velocidad = Column(Integer, nullable=False)
    Apodo = Column(VARCHAR, nullable=False)
    Deleted = Column(Boolean, nullable=False, default=False)
    material_espesor = relationship("TB_MATERIAL_ESPESOR", back_populates="Material")

    def __repr__(self):
        return f"<TB_MATERIALES(id_material={self.id_material}, Nombre={self.Nombre}, Valor={self.Valor}, Velocidad={self.Velocidad}, Apodo={self.Apodo}, Deleted={self.Deleted})>"

class TB_PROYECTOS(Base):
    __tablename__ = 'tb_proyectos'
    id_proyectos = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)
    id_usuario = Column(Integer, ForeignKey("tb_usuarios.id_usuario"), nullable=False)
    id_figura = Column(Integer, ForeignKey("tb_figuras.id_figura"), nullable=False)
    id_descuento = Column(Integer, ForeignKey("tb_descuentos.id_descuento"), nullable=False)
    id_material_espesor = Column(Integer, ForeignKey("tb_material_espesor.id_material_espesor"), nullable=False)
    usuario = relationship("TB_USUARIOS", back_populates="proyectos")
    figura = relationship("TB_FIGURAS", back_populates="proyectos")
    descuento = relationship("TB_DESCUENTOS", back_populates="proyectos")
    material_espesor = relationship("TB_MATERIAL_ESPESOR", back_populates="proyectos")
    Deleted = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<TB_PROYECTOS(id_proyectos={self.id_proyectos}, Cantidad={self.Cantidad}, id_usuario={self.id_usuario}, id_figura={self.id_figura}, id_descuento={self.id_descuento}, id_material_espesor={self.id_material_espesor}, Deleted={self.Deleted})>"

class TB_DESCUENTOS(Base):
    __tablename__ = 'tb_descuentos'
    id_descuento = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)
    Descuento = Column(Integer, nullable=False)
    Deleted = Column(Boolean, nullable=False, default=False)
    proyectos = relationship("TB_PROYECTOS", back_populates="descuento")

    def __repr__(self):
        return f"<TB_DESCUENTOS(id_descuento={self.id_descuento}, Cantidad={self.Cantidad}, Descuento={self.Descuento}, Deleted={self.Deleted})>"

def save():
    Base.metadata.create_all(pool)