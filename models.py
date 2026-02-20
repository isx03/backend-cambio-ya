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

class CuentaBancaria(Base):
    __tablename__ = "cuentas_bancarias"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    bank_name = Column(String(50))
    account_number = Column(String(20))
    currency = Column(String(3))
    account_type = Column(String(20))
