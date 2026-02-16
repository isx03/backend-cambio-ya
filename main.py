# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import SessionLocal, engine, Base
from models import Usuario
from schemas import UsuarioCreate, UsuarioOut

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
