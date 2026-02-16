# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100))
    dni = Column(String(8))
    email = Column(String(50))
    clave = Column(String)
