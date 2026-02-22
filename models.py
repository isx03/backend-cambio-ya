# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float
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

class SimulacionCambio(Base):
    __tablename__ = "simulaciones_cambio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    monto_envio = Column(Float)
    moneda_envio = Column(String(3))
    monto_recibo = Column(Float)
    moneda_recibo = Column(String(3))
    tipo_cambio = Column(Float)
    cuenta_origen_id = Column(Integer, nullable=True)
    cuenta_destino_id = Column(Integer, nullable=True)
    numero_operacion = Column(String(50), nullable=True)
    fecha_simulacion = Column(DateTime, default=datetime.utcnow)