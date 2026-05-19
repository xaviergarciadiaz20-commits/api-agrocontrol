from sqlalchemy import (
    Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, SmallInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False, default="ganadero")
    telefono = Column(String(30), nullable=True)
    activo = Column(SmallInteger, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    fincas = relationship("Finca", back_populates="usuario", cascade="all, delete-orphan")


class Finca(Base):
    __tablename__ = "fincas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    ubicacion = Column(String(200), nullable=True)
    departamento = Column(String(100), nullable=True)
    hectareas = Column(DECIMAL(10, 2), nullable=False, default=0)
    telefono = Column(String(30), nullable=True)
    color = Column(String(20), nullable=False, default="#1b5e20")
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    usuario = relationship("Usuario", back_populates="fincas")
    animales = relationship("Animal", back_populates="finca", cascade="all, delete-orphan")


class Animal(Base):
    __tablename__ = "animales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), nullable=False, unique=True)
    tipo = Column(String(50), nullable=False)
    raza = Column(String(100), nullable=True)
    peso = Column(DECIMAL(8, 2), nullable=False, default=0)
    edad_meses = Column(Integer, nullable=False, default=0)
    estado = Column(String(50), nullable=False, default="Saludable")
    sexo = Column(String(20), nullable=True)
    origen = Column(String(100), nullable=True)
    fecha_ingreso = Column(String(20), nullable=True)
    cond_reproductiva = Column(String(100), nullable=True)
    vacunado = Column(SmallInteger, nullable=False, default=0)
    observaciones = Column(Text, nullable=True)
    finca_id = Column(Integer, ForeignKey("fincas.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    finca = relationship("Finca", back_populates="animales")
    vacunaciones = relationship(
        "Vacunacion", back_populates="animal", cascade="all, delete-orphan"
    )


class Vacunacion(Base):
    __tablename__ = "vacunaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_codigo = Column(
        String(50), ForeignKey("animales.codigo", ondelete="CASCADE"), nullable=False
    )
    vacuna = Column(String(150), nullable=False)
    fecha = Column(String(20), nullable=True)
    proxima_fecha = Column(String(20), nullable=True)
    veterinario = Column(String(100), nullable=True)
    lote = Column(String(100), nullable=True)
    estado = Column(String(50), nullable=False, default="Al día")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    animal = relationship("Animal", back_populates="vacunaciones")
