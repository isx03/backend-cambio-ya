from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre_completo: str
    dni: str
    email: str
    clave: str

class UsuarioOut(BaseModel):
    id: int
    nombre_completo: str
    dni: str
    email: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    clave: str

class Token(BaseModel):
    access_token: str
    token_type: str
    id: int
    nombre_completo: str
    email: str

class CuentaBancariaCreate(BaseModel):
    user_id: int
    bank_name: str
    account_number: str
    currency: str
    account_type: str

class CuentaBancaria(CuentaBancariaCreate):
    id: int

    class Config:
        orm_mode = True

class SimulacionCambioCreate(BaseModel):
    user_id: int
    monto_envio: float
    moneda_envio: str
    monto_recibo: float
    moneda_recibo: str
    tipo_cambio: float
    cuenta_origen_id: Optional[int] = None
    cuenta_destino_id: Optional[int] = None
    numero_operacion: Optional[str] = None

class SimulacionCambioOut(SimulacionCambioCreate):
    id: int
    fecha_simulacion: datetime

    class Config:
        orm_mode = True
