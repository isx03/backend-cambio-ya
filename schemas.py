from pydantic import BaseModel
from typing import Optional

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
