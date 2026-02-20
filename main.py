# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from models import Usuario, CuentaBancaria
from database import SessionLocal, engine, Base
from schemas import UsuarioCreate, UsuarioOut, LoginRequest, Token, CuentaBancariaCreate, CuentaBancaria as CuentaBancariaSchema
from jose import jwt
from datetime import datetime, timedelta

# Configuración JWT
SECRET_KEY = "UTEC-CLOUD-COMPUTING" # En producción usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Pendientes")

origins = ['*'] # Permite que el Api Rest se consuma desde cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    if usuario.clave != request.clave:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={
        "id": usuario.id,
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": usuario.id,
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email
    }

@app.post("/usuarios", response_model=UsuarioOut, status_code=201)
def crear_usuario(u: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario_dni = db.query(Usuario).filter(Usuario.dni == u.dni).first()
    if db_usuario_dni:
        raise HTTPException(status_code=400, detail="El DNI ya esta registrado")
    
    db_usuario_email = db.query(Usuario).filter(Usuario.email == u.email).first()
    if db_usuario_email:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")

    nuevo_usuario = Usuario(
        nombre_completo=u.nombre_completo,
        dni=u.dni,
        email=u.email,
        clave=u.clave
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.post("/bank_accounts", response_model=CuentaBancariaSchema, status_code=201)
def crear_cuenta_bancaria(cuenta: CuentaBancariaCreate, db: Session = Depends(get_db)):
    nueva_cuenta = CuentaBancaria(
        user_id=cuenta.user_id,
        bank_name=cuenta.bank_name,
        account_number=cuenta.account_number,
        currency=cuenta.currency,
        account_type=cuenta.account_type
    )
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta

@app.get("/bank_accounts", response_model=List[CuentaBancariaSchema])
def listar_cuentas_bancarias(user_id: int, db: Session = Depends(get_db)):
    cuentas = db.query(CuentaBancaria)\
        .filter(CuentaBancaria.user_id == user_id)\
        .order_by(CuentaBancaria.id.desc())\
        .all()
    return cuentas
